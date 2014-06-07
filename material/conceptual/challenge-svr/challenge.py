
class Challenge(object):

	def __init__(self, name):
		self.name = name
		
	def handle_query(self, parameters):
		return ("naq", [])
