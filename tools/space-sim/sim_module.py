
class Module(object):
	
	def __init__(self, name, sim):
		self.name = name
		self.sim = sim
	
	def should_think(self):
		return False
	
	def think(self, dt):
		pass
	
	def on_new_entity(self, entity):
		pass
	
	def on_entity_removed(self, entity):
		pass
	
	def save(self):
		return {
			'module-name': self.name
		}
	
	def load(self, blob):
		pass
