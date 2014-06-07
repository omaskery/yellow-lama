
import physical_entities as pe
import computer

class ShipEntity(pe.PhysicalEntity):
	
	def __init__(self, category_uid, instance_uid, sim):
		pe.PhysicalEntity.__init__(self, category_uid, instance_uid, sim)
		
		self.computer = computer.Computer()
		self.computer.on_error = self.on_computer_error
		
		source = """
import computer

class MyProgram(computer.Program):

	def think(self, dt):
		pass
		
program = MyProgram(host_computer)
		"""
		
		self.computer.load(source)
	
	def on_computer_error(self, error):
		print "[ship:computer] error: %s" % str(error)
		self.computer.unload()
	
	def think(self, dt):
		pe.PhysicalEntity.think(self, dt)
		
		self.computer.think(dt)
		#print "[ship:%s] pos: %s" % (self.uid, self.pos.as_tuple())
