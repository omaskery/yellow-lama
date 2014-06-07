
class Program(object):
	
	def __init__(self, host_computer):
		self.computer = host_computer
		
	def think(self, dt):
		pass

class PeripheralInterface(object):
	
	def __init__(self, name, inputs = [], outputs = []):
		self.name = name
		self.inputs = inputs
		self.outputs = outputs
	
	def read(self, input_name):
		if input_name not in self.inputs:
			raise Exception("attempted to access invalid input '%s' of peripheral %s" % (input_name, self.name))
		return self.on_read(input_name)
	
	def write(self, output_name, value):
		if output_name not in self.outputs:
			raise Exception("attempted to access invalid output '%s' of peripheral %s" % (output_name, self.name))
		return self.on_write(output_name, value)
	
	def on_read(self, input_name):
		pass
	
	def on_write(self, output_name, value):
		pass

class Computer(object):
	
	def __init__(self):
		self.source = None
		self.program = None
		self.error = None
		self.cycles = 0
		self.on_error = self.ignore_error
		self.peripherals = {}
	
	def register_peripheral(self, peripheral):
		self.peripherals[peripheral.name] = peripheral
	
	def ignore_error(self, error):
		pass
	
	def load(self, source, absorb_errors = True):
		result = False
		
		self.source = source
		
		try:
			code_locals = {'host_computer':self}
			code_globals = {}
			exec(source, code_globals, code_locals)
			if "program" in code_locals.keys():
				self.program = code_locals['program']
				result = True
		except Exception as error:
			self.error = error
			if not absorb_errors:
				raise
			else:
				self.on_error(error)
			
		return result
	
	def unload(self):
		self.source = None
		self.program = None
	
	def think(self, dt, absorb_errors = True):
		result = False
		
		try:
			if self.program is not None:
				self.program.think(dt)
				self.cycles += 1
			result = True
		except Exception as error:
			self.error = error
			if not absorb_errors:
				raise
			else:
				self.on_error(error)
		
		return result
