#!/usr/bin/env python3


import threading
import socket
import json


def main():
    client = Client(('localhost', 40000))
    client.connect()
    
    while client.running:
        text = input("> ")
        if text.lower() in ('quit', 'close', 'exit'):
            break
        client.send_raw(text)
    
    client.stop()
    
    
class Client(object):
    
    def __init__(self, target):
        self.socket = None
        self.target = target
        self.thread = None
        self.running = False
    
    def connect(self):
        self.socket = socket.socket()
        self.socket.connect(self.target)
        self.socket.settimeout(1.0)
        self.thread = threading.Thread(target=self.listen_thread, name="listen-thread")
        self.rx = b""
        
        self.running = True
        self.thread.start()
    
    def listen_thread(self):
        while self.running:
            try:
                data = self.socket.recv(2048)
                if len(data) < 1:
                    self.stop()
                else:
                    self.rx += data
                    if len(self.rx) >= 4:
                        header = self.rx[0:4]
                        length = 0
                        length += (header[3] << 24)
                        length += (header[2] << 16)
                        length += (header[1] <<  8)
                        length += (header[0] <<  0)
                        if len(self.rx) >= length + 4:
                            message = self.rx[4:length+4].decode()
                            self.rx = self.rx[length+4:]
                            print("\rrx [%s bytes]: " % length, message, "\n> ", end='')
            except socket.timeout:
                pass
    
    def stop(self):
        self.running = False
    
    def send(self, blob):
        message = json.dumps(blob)
        return self.send_raw(message)
    
    def send_raw(self, message):
        length = len(message)
        len_str = "%s%s%s%s" % (
            chr((length >>  0) & 0xFF),
            chr((length >>  8) & 0xFF),
            chr((length >> 16) & 0xFF),
            chr((length >> 24) & 0xFF)
        )
        text = "%s%s" % (len_str, message)
        self.socket.send(text.encode())
    
    
if __name__ == "__main__":
    main()
