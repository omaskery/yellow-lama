
from math_utils import Vector
import entities

class PhysicalEntity(entities.Entity):
	
	def __init__(self, category_uid, instance_uid, sim):
		entities.Entity.__init__(self, category_uid, instance_uid, sim)
		
		self.pos = Vector(0.0, 0.0, 0.0)
		self.vel = Vector(0.0, 0.0, 0.0)
		self.rot = Vector(0.0, 0.0, 0.0)
		self.radius = 1.0
		self.mass = 1.0
	
	def should_think(self):
		return True
	
	def think(self, dt):
		self.pos = self.pos + (self.vel * dt)
	
	def accelerate(self, force, dt):
		acceleration = (force / self.mass) * dt
		self.vel = self.vel + acceleration
	
	def load(self, blob):
		entities.Entity.load(self, blob)
		self.pos = Vector.FromList(blob['physical.pos'])
		self.vel = Vector.FromList(blob['physical.vel'])
		self.rot = Vector.FromList(blob['physical.rot'])
		self.radius = blob['physical.radius']
		self.mass = blob['physical.mass']
	
	def save(self):
		blob = entities.Entity.save(self)
		blob['physical.pos'] = self.pos.as_list()
		blob['physical.vel'] = self.vel.as_list()
		blob['physical.rot'] = self.rot.as_list()
		blob['physical.radius'] = self.radius
		blob['physical.mass'] = self.mass
		return blob
