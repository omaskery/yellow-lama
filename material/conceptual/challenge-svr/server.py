#!/usr/bin/env python

import backend
import alarm

import asyncore as ac
import socket
import random

class BaseState(object):
	def __init__(self, client):
		self.client = client
		
	def handle_message(self, message):
		return None

class AuthUsernameState(BaseState):
	
	def handle_message(self, message):
		parsed = message.split(":")
		
		if len(parsed) < 2:
			self.client.tx("naq", ["not enough parameters"])
			return None
			
		if parsed[0] != "username":
			self.client.tx("naq", ["expected username message"])
			return None
			
		salt = str(random.randint(11111,99999))
		self.client.tx("ack", [salt])
		
		return AuthPasswordState(self.client, parsed[1], salt)

class AuthPasswordState(BaseState):
	
	def __init__(self, client, username, salt):
		BaseState.__init__(self, client)
		self.username = username
		self.salt = salt
		
	def handle_message(self, message):
		parsed = message.split(":")
		
		if len(parsed) < 2:
			self.client.tx("naq", ["not enough parameters"])
			return None
			
		if parsed[0] != "validate":
			self.client.tx("naq", ["expected validate message"])
			return None
			
		if not self.client.server.backend.validate(self.username, parsed[1], self.salt):
			self.client.tx("naq", ["invalid username or password"])
			return None
			
		self.client.tx("ack", [])
		
		return QueryState(self.client, self.username)

class QueryState(BaseState):
	
	def __init__(self, client, username):
		BaseState.__init__(self, client)
		self.username = username
		
	def handle_message(self, message):
		parsed = message.split(":")
		
		if len(parsed) < 2:
			self.client.tx("naq", ["not enough parameters"])
			return None
		
		if parsed[0] == "query":
			challenge = parsed[1]
			
			if challenge in self.client.server.challenges.keys():
				c = self.client.server.challenges[challenge]
				response, payload = c.handle_query(parsed[2:])
				self.client.tx(response, payload)
		else:
			self.client.tx("naq", ["invalid message type"])
			
		return None

class ChallengeConnection(ac.dispatcher_with_send):
	
	def __init__(self, sock, addr, server):
		ac.dispatcher_with_send.__init__(self, sock)
		self.server = server
		self.addr = addr
		self.rxbuf = ""
		self.state = AuthUsernameState(self)
	
	def tx(self, header, params):
		parts = [header] + params
		self.send(":".join(parts) + "\r\n")
	
	def handle_read(self):
		data = self.recv(2048)
		if not data:
			return
		self.rxbuf += data
		while True:
			pos = self.rxbuf.find("\r\n")
			if pos == -1:
				break
			msg = self.rxbuf[:pos]
			self.rxbuf = self.rxbuf[pos+2:]
			self.handle_message(msg)
	
	def handle_message(self, message):
		nextState = None
		if self.state is not None:
			nextState = self.state.handle_message(message)
		if nextState is None:
			self.close()
		else:
			self.state = nextState
	
	def handle_close(self):
		self.close()
		
		print "[%s] disconnected" % self.addr

class ChallengeServer(ac.dispatcher):
	
	def __init__(self, host, port):
		ac.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)
		
		self.backend = backend.DefaultBackend()
		self.challenges = {}
		self.addChallenge(alarm.EasyAlarm())
	
	def addChallenge(self, challenge):
		self.challenges[challenge.name] = challenge
	
	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair[0], pair[1][0]
			print "[%s] connected" % addr
			handler = ChallengeConnection(sock, addr, self)

if __name__ == "__main__":
	server = ChallengeServer('', 40000)
	ac.loop()
