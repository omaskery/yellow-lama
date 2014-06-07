
import math

class Vector(object):
	
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
	
	def magnitude2(self):
		return (self.x**2) + (self.y**2) + (self.z**2)
		
	def magnitude(self):
		return math.sqrt(self.magnitude2())
	
	def normalised(self):
		return (self / self.magnitude())
	
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
	
	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
	
	def __mul__(self, scalar):
		return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
	
	def __div__(self, scalar):
		return Vector(self.x / scalar, self.y / scalar, self.z / scalar)
	
	def as_list(self):
		return [self.x, self.y, self.z]
	
	def as_tuple(self):
		return (self.x, self.y, self.z)
	
	@staticmethod
	def FromList(values):
		return Vector(values[0], values[1], values[2])
