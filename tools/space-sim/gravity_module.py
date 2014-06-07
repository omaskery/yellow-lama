
import physical_entities as pe
import solar_entities as se
import sim_module

class Gravity(sim_module.Module):
	
	def __init__(self, sim):
		sim_module.Module.__init__(self, 'gravity', sim)
		self.solar_bodies = []
		self.general_bodies = []
		self.affected = []
		
		self.simplify = False
	
	def should_think(self):
		return True
		
	def think(self, dt):
		if self.simplify:
			self.think_simple(dt)
		else:
			self.think_complex(dt)
	
	def think_simple(self, dt):
		for solar_body in self.solar_bodies:
			for entity in self.general_bodies:
				self.apply_gravity(solar_body, entity, dt)
	
	def think_complex(self, dt):
		for entity_a in self.affected:
			for entity_b in self.affected:
				if entity_a is entity_b: continue
				
				self.apply_gravity(entity_a, entity_b, dt)
	
	def apply_gravity(self, entity_a, entity_b, dt):
		# F = G m1 m2 / r^2
		G = 6.67E-11
		
		delta = entity_a.pos - entity_b.pos
		distance2 = delta.magnitude2()
		force_magnitude = (G * entity_a.mass * entity_b.mass) / distance2
		
		force = delta.normalised() * force_magnitude
		
		entity_b.accelerate(force, dt)
	
	def on_new_entity(self, entity):
		if isinstance(entity, se.SolarBodyEntity):
			self.solar_bodies.append(entity)
			if not self.simplify:
				self.affected.append(entity)
		elif isinstance(entity, pe.PhysicalEntity):
			self.affected.append(entity)
			self.general_bodies.append(entity)
	
	def on_entity_removed(self, entity):
		if entity in self.solar_bodies:
			self.solar_bodies.remove(entity)
			if not self.simplify:
				self.affected.remove(entity)
		elif entity in self.affected:
			self.affected.remove(entity)
			self.general_bodies.remove(entity)
