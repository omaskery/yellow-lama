from math_utils import Vector, Quaternion
import computer
import math

global Quaternion
global computer
global Vector
global math

class MyProgram(computer.Program):
	STATE_IDLE = 0
	STATE_STOP_THRUSTERS = 1
	STATE_ROTATING = 2
	STATE_STOP_THRUSTERS_AGAIN = 3
	STATE_ACCELERATING = 4
	
	def __init__(self, host_computer):
		computer.Program.__init__(self, host_computer)
		
		global MyProgram
		
		self.state = MyProgram.STATE_STOP_THRUSTERS
		self.timer_end = None
		self.stat_counter = 0.0
		
		self.rotation = Vector(0, 0, 0)
		
		self.rot_period = 10.0
		
		self.timer_end = self.rot_period
		self.computer.write('maneuver', 'thrust', ('rot-rcs-ryl', 1E2))
		self.computer.write('maneuver', 'thrust', ('rot-rcs-lyl', 1E2))

	def think(self, dt):
		gyro = self.computer.read('inertia', 'gyroscope')
		self.rotation += gyro
		
		self.stat_counter += dt
		
		#print "gyro:", gyro, "rotation:", self.rotation
		
		if self.timer_end is not None:
			self.timer_end -= dt
		
		if self.state == MyProgram.STATE_IDLE:
			pass
		elif self.state == MyProgram.STATE_STOP_THRUSTERS:
			if self.timer_end <= 0.0:
				self.timer_end = None
				self.computer.write('maneuver', 'thrust', ('rot-rcs-ryl', 0))
				self.computer.write('maneuver', 'thrust', ('rot-rcs-lyl', 0))
				self.state = MyProgram.STATE_ROTATING
		elif self.state == MyProgram.STATE_ROTATING:
			if self.stat_counter >= 1.0:
				print "rotation z:", (self.rotation.z / math.pi * 180.0)
				self.stat_counter = 0.0
			if self.rotation.z <= (-170.0 / 180.0 * math.pi):
				self.computer.write('maneuver', 'thrust', ('rot-rcs-ryr', 1E2))
				self.computer.write('maneuver', 'thrust', ('rot-rcs-lyr', 1E2))
				self.state = MyProgram.STATE_STOP_THRUSTERS_AGAIN
				self.timer_end = self.rot_period
		elif self.state == MyProgram.STATE_STOP_THRUSTERS_AGAIN:
			if self.timer_end <= 0.0:
				self.computer.write('maneuver', 'thrust', ('rot-rcs-ryr', 0))
				self.computer.write('maneuver', 'thrust', ('rot-rcs-lyr', 0))
				
				self.state = MyProgram.STATE_ACCELERATING
				self.computer.write('maneuver', 'thrust', ('main-engine', 1E5))
				self.timer_end = 120.0
		elif self.state == MyProgram.STATE_ACCELERATING:
			if self.timer_end <= 0.0:
				self.timer_end = None
				self.computer.write('maneuver', 'thrust', ('main-engine', 0))
				self.state = MyProgram.STATE_IDLE
		
program = MyProgram(host_computer)
