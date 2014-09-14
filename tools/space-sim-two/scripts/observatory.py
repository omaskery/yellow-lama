#!/usr/bin/env python

from math_utils import Vector
import datetime
import threading
import asyncore
import pygame
import socket
import json

def now():
    return datetime.datetime.now()

def now_plus(seconds):
    return now() + datetime.timedelta(seconds=seconds)

def circle(screen, colour, position, radius):
    if radius > 1:
        pygame.draw.circle(screen, colour, position, radius)
    else:
        screen.set_at(position, colour)

def circle_on_screen(screen, pos, radius):
    screen_size = screen.get_size()
    centre = Vector(screen_size[0] / 2, screen_size[1] / 2, 0)
    distance2 = (pos - centre).magnitude2()
    return ((distance2 + radius ** 2) < (max(centre.as_tuple()) ** 2))

class KnownEntity(object):
    
    def __init__(self, blob):
        self.category_uid = blob["category"]
        self.name = blob["name"]
        self.pos = Vector.from_list(blob["physical"]["position"])
        self.vel = Vector.from_list(blob["physical"]["velocity"])
        self.radius = blob["physical"]["radius"]
        self.mass = blob["physical"]["mass"]
        
        self.previous = []
    
    def update(self, position):
        if (position - self.pos).magnitude2() > (1E8 ** 2):
            self.previous.append(self.pos)
        self.pos = position
        if len(self.previous) > 200:
            self.previous = self.previous[1:]

class Transmission(object):
    
    def __init__(self, position, radius):
        self.position = position
        self.radius = radius

class Observatory(asyncore.dispatcher_with_send):
    
    def __init__(self,  host, port):
        asyncore.dispatcher_with_send.__init__(self)
        self.rx = ""
        
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        
        self.connected = False
        
        self.zoom = 1E-10
        self.camera = Vector(0, 0, 0)
        
        self.running = True
        self.polling = False
        
        self.network_thread = None
        
        self.verbose = False
        
        self.entities = {}
        self.transmissions = []
        
        self.colours = {
            'Sol' : (255, 255, 0),
            'Mercury' : (100, 50, 50),
            'Venus' : (200, 200, 50),
            'Earth' : (100, 100, 255),
            'Earth.Moon' : (200, 200, 200),
            'Mars' : (200, 0, 0),
            'Jupiter' : (150, 0, 50),
            'Saturn' : (200, 200, 50),
            'Uranus' : (100, 200, 255),
            'Neptune' : (50, 100, 255)
        }
    
    def poll(self):
        self.send_blob({"cmd":"get-entity"})
        self.polling = True
    
    def send_blob(self, blob):
        message = json.dumps(blob)
        header = "%s%s%s%s" % (
            chr((len(message) >>  0) & 0xFF),
            chr((len(message) >>  8) & 0xFF),
            chr((len(message) >> 16) & 0xFF),
            chr((len(message) >> 24) & 0xFF)
        )
        self.send("%s%s" % (header, message))
    
    def start_networking(self):
        self.network_thread = threading.Thread(target = self.networking)
        self.network_thread.setDaemon(True)
        self.network_thread.start()
    
    def handle_connect(self):
        print "[observatory] established connection to simulation"
        self.connected = True
    
    def handle_close(self):
        print "[observatory] lost connection to simulation"
        self.running = False
        self.close()
    
    def handle_read(self):
        data = self.recv(2048)
        if not data: return
        
        self.rx += data
        
        while True:
            if len(self.rx) < 4: break
            
            length = 0
            length += (ord(self.rx[3]) << 24)
            length += (ord(self.rx[2]) << 16)
            length += (ord(self.rx[1]) <<  8)
            length += (ord(self.rx[0]) <<  0)
            
            if len(self.rx) < 4 + length: break
            
            message = json.loads(self.rx[4:length+4])
            self.rx = self.rx[length+4:]
            
            self.handle_message(message)
    
    def handle_message(self, message):
        self.polling = False
        
        entities = message["args"]
        for entity in entities:
            ent = KnownEntity(entity)    
            
            if ent.name in self.entities.keys():
                self.entities[ent.name].update(ent.pos)
            else:
                self.entities[ent.name] = ent
    
    def networking(self):
        asyncore.loop()
    
    def draw(self, screen):
        screen.fill((0,0,0))
        
        for body in self.entities.values():
            pos = body.pos
            radius = body.radius
            
            pos = (pos - self.camera) * self.zoom
            
            radius *= self.zoom
            if radius < 2:
                radius = 2
            
            if not circle_on_screen(screen, pos, radius):
                continue
            
            colour = (255,255,255)
            if body.name in self.colours.keys():
                colour = self.colours[body.name]
            
            circle(screen, colour, (int(pos.x), int(pos.y)), int(radius))
            for old in body.previous:
                pos = (old - self.camera) * self.zoom
                circle(screen, colour, (int(pos.x), int(pos.y)), 1)
        
        pygame.display.flip()

def main():
    pygame.init()
    width, height = (1024, 768)
    screen = pygame.display.set_mode((width, height))
    running = True
    
    observatory = Observatory('localhost', 40000)
    observatory.start_networking()
    
    focus = None
    focus_name = 'Earth'
    
    if focus_name == 'Sol':
        observatory.zoom = 5E-11
    elif focus_name == 'Earth':
        observatory.zoom = 1E-6
    
    clicked = None
    
    poll_rate = 20
    next_poll = now_plus(1.0 / poll_rate)
    
    zoom_rate = 1.05
    large_zoom_rate = zoom_rate * 10
    
    while observatory.running:
        if now() >= next_poll and observatory.connected and not observatory.polling:
            observatory.poll()
            next_poll += datetime.timedelta(seconds = 1.0 / poll_rate)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                observatory.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = event.pos
                elif event.button == 4:
                    observatory.zoom *= zoom_rate
                elif event.button == 5:
                    observatory.zoom /= zoom_rate
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    clicked = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    observatory.zoom *= large_zoom_rate
                elif event.key == pygame.K_q:
                    observatory.zoom /= large_zoom_rate
        
        width_metres = width / observatory.zoom
        height_metres = height / observatory.zoom

        if focus_name in observatory.entities.keys():
            focus = observatory.entities[focus_name]
        
        if focus is not None:
            px, py, pz = focus.pos.as_tuple()
            offset_x, offset_y = width_metres / 2, height_metres / 2
            if clicked is not None:
                cx, cy = clicked
                mx, my = pygame.mouse.get_pos()
                offset_x -= cx - mx
                offset_y -= cy - my
            observatory.camera = Vector(px - offset_x, py - offset_y, 0)
        
        observatory.draw(screen)
    
    observatory.close()
    pygame.quit()

if __name__ == "__main__":
    main()
