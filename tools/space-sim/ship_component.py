
class ShipComponent(object):

	def __init__(self, name):
		self.name = name
		self.mass = 0.0
	
	def think(self, dt):
		pass
		
	def save(self):
		return {
			'name': self.name,
			'mass': self.mass
		}
	
	def load(self, blob):
		self.mass = blob['mass']
