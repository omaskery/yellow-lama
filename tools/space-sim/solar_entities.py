
import physical_entities as pe

class SolarBodyEntity(pe.PhysicalEntity):
	
	def __init__(self, category_uid, instance_uid, sim):
		pe.PhysicalEntity.__init__(self, category_uid, instance_uid, sim)
		
		self.name = ""
	
	def think(self, dt):
		pe.PhysicalEntity.think(self, dt)
	
	def load(self, blob):
		pe.PhysicalEntity.load(self, blob)
		self.name = blob['solar-body.name']
	
	def save(self):
		blob = pe.PhysicalEntity.save(self)
		blob['solar-body.name'] = self.name
		return blob
