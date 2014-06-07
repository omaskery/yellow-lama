
class Entity(object):
	
	def __init__(self, category_uid, instance_uid, sim):
		self.category_uid = category_uid
		self.uid = instance_uid
		self.sim = sim
		self.alive = True
	
	def should_think(self):
		return False
	
	def handle_message(self, source_uid, message):
		pass
	
	def think(self, dt):
		pass
	
	def load(self, blob):
		self.category_uid = blob['category_uid']
		self.uid = blob['instance_uid']
	
	def save(self):
		return {
			'category_uid' : self.category_uid,
			'instance_uid' : self.uid
		}

class EntityFactory(object):
	
	def __init__(self, category_uid, entity_class):
		self.category_uid = category_uid
		self.entity_class = entity_class
	
	def load(self, blob, sim):
		entity = self.entity_class(blob["category_uid"], blob["instance_uid"], sim)
		entity.load(blob)
		return entity
