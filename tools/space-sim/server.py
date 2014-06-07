#!/usr/bin/env python

import threading
import asyncore
import socket
import signal

from math_utils import Vector

import simulation

import physical_entities
import solar_entities
import ship_entity

class Networking(asyncore.dispatcher):
	
	def __init__(self, port, sim):
		asyncore.dispatcher.__init__(self)
		
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(("", port))
		self.listen(10)
		
		self.sim = sim
		self.connections = []
		self.thread = None
	
	def handle_accept(self):
		sock, (address, garbage) = self.accept()
		
		connection = Client(sock, address, self, self.sim)
		
		self.connections.append(connection)
	
	def handle_disconnect(self, connection):
		if connection in self.connections:
			self.connections.remove(connection)
	
	def start(self):
		self.thread = threading.Thread(target = self.run)
		self.thread.setDaemon(True)
		self.thread.start()
	
	def run(self):
		asyncore.loop()

class Client(asyncore.dispatcher_with_send):
	
	def __init__(self, sock, address, server, sim):
		asyncore.dispatcher_with_send.__init__(self, sock)
		
		self.address = address
		self.server = server
		self.sim = sim
		self.rx = ""
		
		print "[%s] connected" % self.address
	
	def handle_read(self):
		data = self.recv(2048)
		if not data: return
		
		self.rx += data
		
		while True:
			pos = self.rx.find("\r\n")
			if pos == -1: break
			
			message = self.rx[:pos]
			self.rx = self.rx[pos + 2:]
			
			self.handle_message(message)
	
	def handle_message(self, message):
		tokens = message.split()
		if len(tokens) < 1: return
		
		if tokens[0] == 'list-physical':
			information = []
			for body in self.sim.modules['gravity'].solar_bodies:
				information.append("solar-body:%s,%s,%s,%s,%s,%s,%s,%s" % (
					body.name,
					body.category_uid,
					body.uid,
					body.pos.x, body.pos.y, body.pos.z,
					body.radius,
					body.mass
				))
			for body in self.sim.modules['gravity'].general_bodies:
				information.append("general-body:%s,%s,%s,%s,%s,%s,%s" % (
					body.category_uid,
					body.uid,
					body.pos.x, body.pos.y, body.pos.z,
					body.radius,
					body.mass
				))
			self.send("%s\r\n" % "#".join(information))
		else:
			print "[%s] rx: %s" % (self.address, tokens)
	
	def handle_close(self):
		print "[%s] disconnected" % self.address
		self.do_close()
	
	def do_close(self):
		self.server.handle_disconnect(self)
		self.close()

class SignalHandler(object):
	
	def __init__(self, sim):
		self.sim = sim
	
	def handle(self, signal, frame):
		print "\r[space-sim] keyboard interrupt caught, signalling stop"
		self.sim.stop()

def main():
	state_file = "sim.state"
	load_state = False
	save_state = True
	
	print "[space-sim] starting"
	sim = simulation.Simulation()
	server = Networking(8000, sim)
	
	signal_handler = SignalHandler(sim)
	
	sim.register_entity_category('spaceship', ship_entity.ShipEntity)
	sim.register_entity_category('solar-body', solar_entities.SolarBodyEntity)
	
	if load_state:
		print "[space-sim] loading state"
		sim.load(state_file)
	else:
		print "[space-sim] generating state"
		
		solar_bodies = [
			{
				'name': 'Sol',
				'pos': Vector(0, 0, 0),
				'vel': Vector(0, 0, 0),
				'mass': 1.9891E30,
				'radius': 695500E3
			},
			#{
			#	'name': 'BlackHole',
			#	'pos': Vector(-2.4E20, 0, 0),
			#	'vel': Vector(0, 0, 0),
			#	'mass': 7.9564E34,
			#	'radius': 6.7453303E12
			#},
			{
				'name': 'Mercury',
				'pos': Vector(5.791000e+10, 0, 0),
				'vel': Vector(0, -47.36E3, 0),
				'mass': 328.5E21,
				'radius': 2440E3
			},
			{
				'name': 'Venus',
				'pos': Vector(1.082000e+11, 0, 0),
				'vel': Vector(0, -35.02E3, 0),
				'mass': 4.867E24,
				'radius': 6052E3
			},
			{
				'name': 'Earth',
				'pos': Vector(149.59787E9, 0, 0),
				'vel': Vector(0, -29.77E3, 0),
				'mass': 5.97219E24,
				'radius': 6378.1E3
			},
			{
				'name': 'Earth.Moon',
				'pos': Vector(149.59787E9 + 385E6, 0, 0),
				'vel': Vector(0, -29.77E3 + -1020, 0),
				'mass': 7.34767309E22,
				'radius': 1737.4E3
			},
			{
				'name': 'Mars',
				'pos': Vector(2.279000e+11, 0, 0),
				'vel': Vector(0, -24.07E3, 0),
				'mass': 6.4174E23,
				'radius': 3389.5E3
			},
			{
				'name': 'Jupiter',
				'pos': Vector(7.785000e+11, 0, 0),
				'vel': Vector(0, -13.06E3, 0),
				'mass': 1.898E27,
				'radius': 69911E3
			},
			{
				'name': 'Saturn',
				'pos': Vector(1.433000e+12, 0, 0),
				'vel': Vector(0, -9.68E3, 0),
				'mass': 568.3E24,
				'radius': 58232E3
			},
			{
				'name': 'Uranus',
				'pos': Vector(2.877000e+12, 0, 0),
				'vel': Vector(0, -6.8E3, 0),
				'mass': 86.81E24,
				'radius': 25362E3
			},
			{
				'name': 'Neptune',
				'pos': Vector(4.503000e+12, 0, 0),
				'vel': Vector(0, -5.43E3, 0),
				'mass': 102.4E24,
				'radius': 24622E3
			}
		]
		
		for body in solar_bodies:
			planet = solar_entities.SolarBodyEntity('solar-body', sim.allocate_uid(), sim)
			planet.name = body['name']
			planet.pos = body['pos']
			planet.vel = body['vel']
			planet.mass = body['mass']
			planet.radius = body['radius']
			sim.add_entity(planet)
		
		ship = ship_entity.ShipEntity('spaceship', sim.allocate_uid(), sim)
		
		ship.pos = Vector(149.59787E9 + 6378.1E3 + 370E3, 0, 0) # around the earth
		ship.vel.y = -29.77E3 + -7.7E3 # Hopefully in orbit
		
		sim.add_entity(ship)
	
	print "[space-sim] hooking SIGINT"
	signal.signal(signal.SIGINT, signal_handler.handle)
	
	print "[space-sim] starting networking"
	server.start()
	
	print "[space-sim] entering simulation loop"
	while sim.running:
		sim.update()
	
	if save_state:
		print "[space-sim] saving state"
		sim.save(state_file)
	
	print "[space-sim] shutting down"

if __name__ == "__main__":
	main()
