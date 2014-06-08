
from math_utils import Vector, Quaternion
import entities

class PhysicalEntity(entities.Entity):
	
	def __init__(self, category_uid, instance_uid, sim):
		entities.Entity.__init__(self, category_uid, instance_uid, sim)
		
		self.pos = Vector(0.0, 0.0, 0.0)
		self.vel = Vector(0.0, 0.0, 0.0)
		self.rot = Quaternion.from_angle_and_axis(0.0, Vector(0, 0, 1))
		self.rotvel = Quaternion.from_angle_and_axis(0.0, Vector(0.0, 0.0, 1.0))
		self.radius = 1.0
		self.mass = 1.0
	
	def should_think(self):
		return True
	
	def think(self, dt):
		self.pos = self.pos + (self.vel * dt)
		self.rot = self.rot * (self.rotvel ** dt)
	
	def accelerate(self, force, dt):
		acceleration = (force / self.mass) * dt
		self.vel = self.vel + acceleration
	
	def apply_moment(self, angular_acceleration, dt):
		#print "angular e:", angular_acceleration.as_tuple()
		q = Quaternion.from_euler_rotation(angular_acceleration)
		#print "angular q:", q.as_tuple()
		self.rotvel = self.rotvel * q ** 2
		#print "rotvel  q:", self.rotvel.as_tuple()
		#print "rotvel  e:", self.rotvel.to_euler_angle().as_tuple()
	
	def load(self, blob):
		entities.Entity.load(self, blob)
		self.pos = Vector.from_list(blob['physical.pos'])
		self.vel = Vector.from_list(blob['physical.vel'])
		self.rot = Quaternion.from_list(blob['physical.rot'])
		self.rotvel = Quaternion.from_list(blob['physical.rotvel'])
		self.radius = blob['physical.radius']
		self.mass = blob['physical.mass']
	
	def save(self):
		blob = entities.Entity.save(self)
		blob['physical.pos'] = self.pos.as_list()
		blob['physical.vel'] = self.vel.as_list()
		blob['physical.rot'] = self.rot.as_list()
		blob['physical.rotvel'] = self.rotvel.as_list()
		blob['physical.radius'] = self.radius
		blob['physical.mass'] = self.mass
		return blob
