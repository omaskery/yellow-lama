
import physical_entities as pe
from math_utils import *
import computer
import logging

class ManeuverPeripheral(computer.PeripheralInterface):
	
	def __init__(self, ship):
		computer.PeripheralInterface.__init__(self, 'maneuver')
		self.inputs['max-thrust'] = self.get_max_thrust
		self.outputs['thrust'] = self.set_thrust
		self.outputs['moment'] = self.apply_moment
		self.ship = ship
		
		self.max_rcs_thrust = 10 # newtons
		self.max_main_thrust = 1E4 # newtons
		
		self.max_thrust = [
			(-self.max_rcs_thrust,  self.max_rcs_thrust), # left, right
			(-self.max_main_thrust, self.max_rcs_thrust), # forward, backward
			(-self.max_rcs_thrust,  self.max_rcs_thrust)  # down, up
		]
	
	def get_max_thrust(self, value_name):
		return self.max_thrust
	
	def set_thrust(self, value_name, value):
		self.ship.thrust.x = clamp(value.x, self.max_thrust[0][0], self.max_thrust[0][1])
		self.ship.thrust.y = clamp(value.y, self.max_thrust[1][0], self.max_thrust[1][1])
		self.ship.thrust.z = clamp(value.z, self.max_thrust[2][0], self.max_thrust[2][1])
		print "[ship:maneuver] set thrust to %s" % (self.ship.thrust.as_tuple(),)
	
	def apply_moment(self, value_name, value):
		pass

class ShipEntity(pe.PhysicalEntity):
	
	def __init__(self, category_uid, instance_uid, sim):
		pe.PhysicalEntity.__init__(self, category_uid, instance_uid, sim)
		
		self.computer = computer.Computer()
		self.computer.register_peripheral(ManeuverPeripheral(self))
		self.computer.on_error = self.on_computer_error
		self.thrust = Vector(0, 0, 0)
		
		source = """
from math_utils import Vector
import computer

class MyProgram(computer.Program):

	def __init__(self, host_computer):
		global computer
		global Vector
		
		computer.Program.__init__(self, host_computer)
		
		self.time = 0.0
		self.thrust_engaged = True
		self.computer.write('maneuver', 'thrust', Vector(0, -1E4, 0))

	def think(self, dt):
		self.time += dt
		if self.time > 120.0 and self.thrust_engaged:
			self.thrust_engaged = False
			self.computer.write('maneuver', 'thrust', Vector(0,0,0))
		
program = MyProgram(host_computer)
		"""
		
		self.computer.load(source)
	
	def on_computer_error(self, error):
		print "[ship:computer] error: %s" % (error,)
		logging.exception("ship computer exception")
		self.computer.unload()
	
	def think(self, dt):
		pe.PhysicalEntity.think(self, dt)
		
		force = self.rot.rotate_vector(self.thrust)
		self.accelerate(force, dt)
		
		self.computer.think(dt)
		#print "[ship:%s] pos: %s" % (self.uid, self.pos.as_tuple())
	
	def save(self):
		blob = pe.PhysicalEntity.save(self)
		blob['ship.computer.source'] = self.computer.source
		blob['ship.thrust'] = self.thrust.as_list()
		return blob
	
	def load(self, blob):
		pe.PhysicalEntity.load(self, blob)
		self.computer.load(blob['ship.computer.source'])
		self.thrust = Vector.from_list(blob['ship.thrust'])
