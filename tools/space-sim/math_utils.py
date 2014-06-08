
import math

def clamp(value, lower, upper):
	return max(lower, min(value, upper))

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
	
	def dot_product(self, other):
		return (self.x * other.x + self.y * other.y + self.z * other.z)
	
	def cross_product(self, other):
		return Vector(
			self.y * other.z - self.z * other.y,
			self.z * other.x - self.x * other.z,
			self.x * other.y - self.y * other.x
		)
	
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
	def from_list(values):
		return Vector(values[0], values[1], values[2])

class Quarternion(object):
	
	def __init__(self, w, x, y, z):
		self.w = w
		self.v = Vector(x, y, z)
		
	def inverse(self):
		return Quarternion(self.w, -self.v.x, -self.v.y, -self.v.z)
	
	def __mul__(self, other):
		sv = self.v
		sw = self.w
		ov = other.v
		ow = other.w
		
		w = sw * ow - (sv.dot_product(ov))
		v = sv * ow + ov * sw + sv.cross_product(ov)
		
		return Quarternion(w, v.x, v.y, v.z)
	
	def __pow__(self, exponent):
		theta, axis = self.to_angle_and_axis()
		
		return Quarternion.from_angle_and_axis(theta * exponent, axis)
	
	def slerp(self, other, t):
		return (((other * self.inverse()) ** t) * self)
	
	def rotate_vector(self, vector):
		qv = Quarternion(0, vector.x, vector.y, vector.z) # vector as quarternion
		vc_vector = self.v.cross_product(vector)
		return (vector + (vc_vector * (2 * self.w)) + (self.v.cross_product(vc_vector) * 2))
	
	def as_list(self):
		return [self.w, self.v.x, self.v.y, self.v.z]
	
	def as_tuple(self):
		return (self.w, self.v.x, self.v.y, self.v.z)
	
	def to_angle_and_axis(self):
		half_theta = math.acos(self.w)
		theta = 2.0 * half_theta
		if self.v.magnitude2() < 0.0001:
			axis = Vector(1, 0, 0)
		else:
			axis = self.v.normalised()
		return (theta, axis)
	
	@staticmethod
	def from_angle_and_axis(theta, axis):
		half_theta = theta / 2
		w = math.cos(half_theta)
		scaled_axis = axis * math.sin(half_theta)
		return Quarternion(w, scaled_axis.x, scaled_axis.y, scaled_axis.z)
	
	@staticmethod
	def from_list(self, values):
		return Quarternion(values[0], values[1], values[2], values[3])
