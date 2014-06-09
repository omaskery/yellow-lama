
import physical_entities as pe
from math_utils import *
import ship_component
import computer
import logging

default_ship_computer_source = open('default_ship_computer_source.py', 'r').read()

class ManeuverPeripheral(computer.PeripheralInterface):
	
	def __init__(self, ship):
		computer.PeripheralInterface.__init__(self, 'maneuver')
		self.inputs['max-thrust'] = self.get_max_thrust
		self.outputs['thrust'] = self.set_thrust
		self.ship = ship
	
	def get_max_thrust(self, value_name):
		max_thrusts = {}
		for thruster in self.thrusters:
			max_thrusts[thruster.name] = thruster.max_force
		return max_thrusts
	
	def set_thrust(self, value_name, value):
		thruster_name, thrust_value = value
		for thruster in self.ship.thrusters:
			if thruster.name == thruster_name:
				thruster.set_thrust(thrust_value)
				break

class InertiaPeripheral(computer.PeripheralInterface):
	
	def __init__(self, accel, gyro):
		computer.PeripheralInterface.__init__(self, 'inertia')
		self.inputs['accelerometer'] = self.get_accelerometer_data
		self.inputs['gyroscope'] = self.get_gyroscope_data
		self.accel = accel
		self.gyro = gyro
	
	def get_accelerometer_data(self, value_name):
		return self.accel.latest()
	
	def get_gyroscope_data(self, value_name):
		return self.gyro.latest()

class AccelerometerComponent(ship_component.ShipComponent):
	
	def __init__(self, ship, name = "accelerometer"):
		ship_component.ShipComponent.__init__(self, name)
		
		self.ship = ship
		self.latest_value = Vector(0,0,0)
		self.positions = []
	
	def think(self, dt):
		if len(self.positions) == 2:
			delta_a = self.positions[1] - self.positions[0]
			delta_b = self.ship.pos - self.positions[1]
			delta = delta_b - delta_a
			self.latest_value = delta
		
		self.positions.append(Vector.from_list(self.ship.pos.as_list()))
		if len(self.positions) > 2:
			self.positions = self.positions[1:]
	
	def latest(self):
		return self.latest_value
	
	def save(self):
		blob = ship_component.ShipComponent.save(self)
		return blob
		
	def load(self, blob):
		ship_component.ShipComponent.load(self, blob)

class GyroscopeComponent(ship_component.ShipComponent):
	
	def __init__(self, ship, name = "gyroscope"):
		ship_component.ShipComponent.__init__(self, name)
		
		self.ship = ship
		self.latest_value = Vector(0,0,0)
		self.last_rotation = None
		
	def think(self, dt):
		if self.last_rotation is not None:
			#print "gyroscope:"
			#print "last:", self.last_rotation
			#print "ship:", self.ship.rot
			delta = self.ship.rot.difference(self.last_rotation)
			#print "delta:", delta
			self.latest_value = delta.to_euler_angle()
			#print "delta:", self.latest_value
		self.last_rotation = Quaternion.from_list(self.ship.rot.as_list())
	
	def latest(self):
		return self.latest_value
	
	def save(self):
		blob = ship_component.ShipComponent.save(self)
		return blob
		
	def load(self, blob):
		ship_component.ShipComponent.load(self, blob)

class ComputerComponent(ship_component.ShipComponent):
	
	def __init__(self, ship, name = "computer"):
		ship_component.ShipComponent.__init__(self, name)
		
		self.ship = ship
		self.computer = computer.Computer()
		self.computer.register_peripheral(ManeuverPeripheral(self.ship))
		self.computer.register_peripheral(InertiaPeripheral(self.ship.accelerometer, self.ship.gyroscope))
		self.computer.on_error = self.on_computer_error
		
		self.computer.load(default_ship_computer_source)
	
	def on_computer_error(self, error):
		print "[ship:computer] error: %s" % (error,)
		logging.exception("ship computer exception")
		self.computer.unload()
	
	def think(self, dt):
		self.computer.think(dt)
	
	def save(self):
		blob = ship_component.ShipComponent.save(self)
		blob['computer.source'] = self.computer.source
		return blob
	
	def load(self, blob):
		ship_component.ShipComponent.load(self, blob)
		self.computer.load(blob['computer.source'])

class ThrusterComponent(ship_component.ShipComponent):
	
	def __init__(self, name, ship, direction, offset, max_force):
		ship_component.ShipComponent.__init__(self, name)
		
		self.ship = ship
		self.direction = direction
		self.max_force = max_force
		self.offset = offset
		self.debug = False
		
		self.thrust = 0.0
	
	def set_thrust(self, thrust):
		self.thrust = clamp(thrust, 0.0, self.max_force)
		print "[thruster:%s] set to %s N" % (self.name, self.thrust)
	
	def linear_thrust(self):
		result = self.direction * self.thrust
		return result
	
	def angular_acceleration(self):
		calc = self.single_torque_calculation
		result = Vector(
			calc(self.direction.y, self.offset.z)\
			 + calc(self.direction.z, self.offset.y),
			calc(self.direction.x, self.offset.z)\
			 + calc(self.direction.z, self.offset.x),
			calc(self.direction.x, self.offset.y)\
			 + calc(self.direction.y, self.offset.x)
		)
		return result
	
	def single_torque_calculation(self, perpendicular, radius):
		if abs(radius) < 0.0001:
			if self.debug:
				print "[thruster:%s] radius ~0" % self.name
			return 0.0
		else:
			result = (perpendicular * radius * self.thrust) / (self.ship.mass * radius ** 2)
			if self.debug:
				print "[thruster:%s] (%s * %s * %s) / (%s * %s) = %s" % (
					self.name, perpendicular, radius, self.thrust,
					self.ship.mass, radius ** 2, result
				)
			return result
	
	def think(self, dt):
		pass
	
	def save(self):
		blob = ship_component.ShipComponent.save(self)
		blob['direction'] = self.direction.as_list()
		blob['max_force'] = self.max_force
		blob['thrust'] = self.thrust
		blob['offset'] = self.offset
	
	def load(self, blob):
		ship_component.ShipComponent.load(self, blob)
		self.direction = Vector.from_list(blob['direction'])
		self.max_force = blob['max_force']
		self.thrust = blob['thrust']
		self.offset = Vector.from_list(blob['offset'])

class ShipEntity(pe.PhysicalEntity):
	
	def __init__(self, category_uid, instance_uid, sim):
		pe.PhysicalEntity.__init__(self, category_uid, instance_uid, sim)
		
		self.rot *= Quaternion.from_angle_and_axis(math.pi, Vector(0,0,1))
		
		self.components = {}
		
		lin_rcs_thrust = 1E2
		rot_rcs_thrust = 3E1
		main_engine_thrust = 1E5
		
		self.thrusters = [
			ThrusterComponent('lin-rcs-f', self,   Vector( 0.0, 1.0, 0.0), Vector( 0,-1, 0), lin_rcs_thrust),
			ThrusterComponent('lin-rcs-b', self,   Vector( 0.0,-1.0, 0.0), Vector( 0, 1, 0), lin_rcs_thrust),
			ThrusterComponent('lin-rcs-l', self,   Vector(-1.0, 0.0, 0.0), Vector( 1, 0, 0), lin_rcs_thrust),
			ThrusterComponent('lin-rcs-r', self,   Vector( 1.0, 0.0, 0.0), Vector(-1, 0, 0), lin_rcs_thrust),
			ThrusterComponent('lin-rcs-u', self,   Vector( 0.0, 0.0, 1.0), Vector( 0, 0,-1), lin_rcs_thrust),
			ThrusterComponent('lin-rcs-d', self,   Vector( 0.0, 0.0,-1.0), Vector( 0, 0, 1), lin_rcs_thrust),
			
			ThrusterComponent('rot-rcs-fpb', self, Vector( 0.0, 0.0, 1.0), Vector( 0, 1, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-fpf', self, Vector( 0.0, 0.0,-1.0), Vector( 0, 1, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-bpb', self, Vector( 0.0, 0.0, 1.0), Vector( 0,-1, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-bpf', self, Vector( 0.0, 0.0,-1.0), Vector( 0,-1, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-lrr', self, Vector( 0.0, 0.0, 1.0), Vector(-1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-lrl', self, Vector( 0.0, 0.0,-1.0), Vector(-1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-rrr', self, Vector( 0.0, 0.0,-1.0), Vector( 1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-rrl', self, Vector( 0.0, 0.0, 1.0), Vector( 1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-lyl', self, Vector( 0.0,-1.0, 0.0), Vector(-1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-lyr', self, Vector( 0.0, 1.0, 0.0), Vector(-1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-ryl', self, Vector( 0.0, 1.0, 0.0), Vector( 1, 0, 0), rot_rcs_thrust),
			ThrusterComponent('rot-rcs-ryr', self, Vector( 0.0,-1.0, 0.0), Vector( 1, 0, 0), rot_rcs_thrust),
			
			ThrusterComponent('main-engine', self, Vector( 0.0, 1.0, 0.0), Vector( 0,-1, 0), main_engine_thrust)
		]
		
		self.accelerometer = AccelerometerComponent(self)
		self.gyroscope = GyroscopeComponent(self)
		self.computer = ComputerComponent(self)
		
		self.register_component(self.accelerometer)
		self.register_component(self.gyroscope)
		self.register_component(self.computer)
		for thruster in self.thrusters:
			self.register_component(thruster)
	
	def register_component(self, component):
		self.components[component.name] = component
	
	def think(self, dt):
		pe.PhysicalEntity.think(self, dt)
		
		for component in self.components.values():
			component.think(dt)
		
		thrust = sum([thruster.linear_thrust() for thruster in self.thrusters], Vector(0,0,0))
		self.accelerate(self.rot.rotate_vector(thrust), dt)
		
		torque = sum([thruster.angular_acceleration() for thruster in self.thrusters], Vector(0,0,0))
		#print "net torque:", torque.as_tuple()
		self.apply_moment(self.rot.rotate_vector(torque), dt)
	
	def save(self):
		blob = pe.PhysicalEntity.save(self)
		for component in self.components.keys():
			component_blob = self.components[component].save()
			blob['ship.component.' + component] = component_blob
		return blob
	
	def load(self, blob):
		pe.PhysicalEntity.load(self, blob)
		for component in self.components.keys():
			component_blob = blob['ship.component.' + component]
			self.components[component].load(component_blob)
