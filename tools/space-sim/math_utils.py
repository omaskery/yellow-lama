#!/usr/bin/env python

import math

def clamp(value, lower, upper):
	return max(lower, min(value, upper))

class Vector(object):
	
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
	
	def __str__(self):
		return "(%02.2f, %02.2f, %02.2f)" % (self.x, self.y, self.z)
	
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

class Quaternion(object):
	
	def __init__(self, w, x, y, z):
		self.w = w
		self.v = Vector(x, y, z)
	
	def __str__(self):
		return "(%02.2f, %02.2f, %02.2f, %02.2f)" % (self.w, self.v.x, self.v.y, self.v.z)
		
	def inverse(self):
		return Quaternion(self.w, -self.v.x, -self.v.y, -self.v.z)
	
	def __mul__(self, other):
		sv = self.v
		sw = self.w
		ov = other.v
		ow = other.w
		
		w = sw * ow - (sv.dot_product(ov))
		v = sv * ow + ov * sw + sv.cross_product(ov)
		
		return Quaternion(w, v.x, v.y, v.z)
	
	def __pow__(self, exponent):
		theta, axis = self.to_angle_and_axis()
		
		return Quaternion.from_angle_and_axis(theta * exponent, axis)
	
	def difference(self, other):
		return (other * self.inverse())
	
	def slerp(self, other, t):
		return ((self.difference(other) ** t) * self)
	
	def rotate_vector(self, vector):
		qv = Quaternion(0, vector.x, vector.y, vector.z) # vector as quarternion
		vc_vector = self.v.cross_product(vector)
		return (vector + (vc_vector * (2 * self.w)) + (self.v.cross_product(vc_vector) * 2))
	
	def as_list(self):
		return [self.w, self.v.x, self.v.y, self.v.z]
	
	def as_tuple(self):
		return (self.w, self.v.x, self.v.y, self.v.z)
	
	def to_angle_and_axis(self):
		if self.v.magnitude2() < 0.0001:
			axis = Vector(1, 0, 0)
		else:
			axis = self.v.normalised()
		
		theta = None
		w = self.w
		try:
			theta = math.acos(clamp(self.w, -1.0, 1.0)) * 2
		except ValueError:
			print self.w, w
			raise
		
		return (theta, axis)
	
	def to_euler_angle(self):
		heading, attitude, bank = None, None, None
		
		abcd = self.w * self.v.x + self.v.y * self.v.z
		
		if abcd > 0.499: # singularity at north pole
			yaw = 2 * math.atan2(self.v.y, self.w)
			pitch = math.pi
			roll = 0
		elif abcd < -0.499: # singularity at south pole
			yaw = -2 * math.atan2(self.v.y, self.w)
			pitch = -math.pi
			roll = 0
		else:
			adbc = self.w * self.v.z - self.v.x * self.v.y
			acbd = self.w * self.v.y - self.v.x * self.v.z
			yaw = math.atan2(2 * adbc, 1 - 2 * (self.v.z ** 2 + self.v.x ** 2))
			unitLength = self.w ** 2 + self.v.x ** 2 + self.v.y ** 2 + self.v.z ** 2
			pitch = math.asin(2 * abcd / unitLength)
			roll = math.atan2(2 * acbd, 1 - 2 * (self.v.y ** 2 + self.v.x ** 2))
		
		return Vector(pitch, roll, yaw)
		
	@staticmethod
	def from_angle_and_axis(theta, axis):
		half_theta = theta / 2
		w = math.cos(half_theta)
		scaled_axis = axis * math.sin(half_theta)
		return Quaternion(w, scaled_axis.x, scaled_axis.y, scaled_axis.z)
	
	@staticmethod
	def from_list(values):
		return Quaternion(values[0], values[1], values[2], values[3])
	
	@staticmethod
	def from_euler_rotation(vector):
		rot_x = Quaternion.from_angle_and_axis(vector.x, Vector(1,0,0))
		rot_y = Quaternion.from_angle_and_axis(vector.y, Vector(0,1,0))
		rot_z = Quaternion.from_angle_and_axis(vector.z, Vector(0,0,1))
		return (rot_z * rot_y * rot_x)

if __name__ == "__main__":
	print "running math utils scratchpad"
	
	class Thruster(object):
		
		def __init__(self, offset, direction, thrust):
			self.offset = offset
			self.direction = direction
			self.thrust = thrust
		
		def linear_thrust(self):
			return self.direction * self.thrust
		
		def angular_torque(self):
			return Vector(
				self.direction.y * self.offset.z + self.direction.z * self.offset.y,
				self.direction.x * self.offset.z + self.direction.z * self.offset.x,
				self.direction.x * self.offset.y + self.direction.y * self.offset.x
			)
		
		def show_info(self):
			linear = self.linear_thrust().as_tuple()
			print "  linear thrust:", linear
			angular = self.angular_torque().as_tuple()
			print "  angular torque:", angular
	
	up = Vector(0,0,1)
	right = Vector(1,0,0)
	forward = Vector(0,1,0)
	
	print "rear thruster:"
	rear_thruster = Thruster(Vector(0,-1,0), Vector(0,1,0), 10000.0)
	rear_thruster.show_info()
	
	print "rear pitch-forward RCS (rot_rcs_pf):"
	rot_rcs_pf = Thruster(Vector(0,-1,0), Vector(0,0,1), 2.0)
	rot_rcs_pf.show_info()
	
	print "right roll-left RCS (rot_rcs_rl):"
	rot_rcs_rl = Thruster(Vector(1,0,0), Vector(0,0,1), 2.0)
	rot_rcs_rl.show_info()
	
	print "front-right roll-pitch-up RCS (rot_rcs_rpu):"
	rot_rcs_rpu = Thruster(Vector(1,1,0), Vector(0,0,1), 2.0)
	rot_rcs_rpu.show_info()
