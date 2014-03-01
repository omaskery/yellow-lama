
ROOM_TEMPERATURE = 26
BOILING_TEMPERATURE = 100
DANGER_TEMPERATURE = 45 # guesstimate at when something hurts
DRINKABLE_TEMPERATURE = 60 # according to like the NHS, seems hot!

def introduce_simulator():
	print("WELCOME TO THE XTREME KETTLE SIMULATOR 3000")
	print("THE FUTURE OF KETTLE SIMULATION IS HERE")

class SimulationContext(object):
	def __init__(self):
		self.tick_count = 0
		self.objects = []
		self.running = False
	def tick(self):
		for obj in self.objects:
			obj.tick(self)
		self.tick_count += 1
	def add(self, obj):
		self.objects.append(obj)

class SimulationObject(object):
	def __init__(self, name):
		self.name = name
	def tick(self, simulation):
		pass

class ContainerException(Exception):
	pass

class ContainerOverfilledException(ContainerException):
	pass

class ContainerObject(object):
	def __init__(self, capacity):
		self.capacity = capacity
		self.contains = 0
	def accept(self, amount):
		space = self.capacity - self.contains
		accepted = amount
		if space > amount:
			accepted = self.capacity - self.contains
			self.contains = self.capacity
			raise ContainerOverfilledException()
		else:
			self.contains += accepted
		return accepted
	def dispense(self, amount):
		dispensed = amount
		if dispensed > self.contains:
			dispensed = self.contains
		self.contains -= dispensed
		return dispensed
	def is_empty(self):
		return (self.contains <= 0)

class KettleException(Exception):
	pass

class Kettle(SimulationObject):
	def __init__(self, name = "Kettle"):
		SimulationObject.__init__(self, name)
		self.water = ContainerObject(5)
		self.temperature = ROOM_TEMPERATURE
		self.turned_on = False
		self.boil_rate = 1 # degrees per simulation tick
		self.cool_rate = 0.01 # degrees per simulation tick
		self.broken = False
	def tick(self, simulation):
		if self.broken:
			raise KettleException("Stop trying to use a broken kettle!")
			
		if self.turned_on:
			if self.water.is_empty():
				self.broken = True
				raise KettleException("BOOM! Kettle set to boil with no water! Your kettle broke.")
			self.temperature += self.boil_rate
			if self.temperature > BOILING_TEMPERATURE:
				self.turn_off()
		elif self.temperature >= ROOM_TEMPERATURE:
			self.temperature -= self.cool_rate
	def is_boiled(self):
		return (self.temperature >= BOILING_TEMPERATURE)
	def is_empty(self):
		return self.water.is_empty()
	def turn_on(self):
		self.turned_on = True
	def turn_off(self):
		self.turned_on = False
	def fill(self, water_amount):
		try:
			self.water.accept(water_amount)
		except ContainerOverfilledException:
			raise KettleException("Splash! You overfilled the kettle, water is everywhere!")
	def fill_completely(self):
		amount = self.water.contains
		try:
			self.water.accept(self.water.capacity)
		except ContainerOverfilledException:
			if amount <= self.water.capacity:
				raise KettleException("Splash! You overfilled the kettle, water is everywhere!")
			else:
				raise KettleException("Splash! There's water everywhere, the kettle was already full!")
	def pour_cup(self, cup):
		if self.water.is_empty():
			raise KettleException("Distressingly when you pour the kettle nothing comes out, there was no water in it!")
		
		dispensed = self.water.dispense(1)
		cup.fill(dispensed, self.temperature)

class CupException(Exception):
	pass

class Cup(SimulationObject):
	def __init__(self, name = "Cup"):
		SimulationObject.__init__(self, name)
		self.contents = ContainerObject(1)
		self.temperature = None
		self.cool_rate = 0.01 # degrees per simulation tick
	def tick(self, simulation):
		if not self.contents.is_empty() and self.temperature >= ROOM_TEMPERATURE:
			self.temperature -= self.cool_rate
	def fill(self, water_amount, water_temperature):
		try:
			self.contents.accept(water_amount)
			self.temperature = water_temperature
		except ContainerOverfilledException:
			if water_temperature >= DANGER_TEMPERATURE:
				raise CupException("Argh! Really hot water overfills the cup!")
			else:
				raise CupException("Argh! Water overfilfs the cup! Luckily it's not too hot.")
				
introduce_simulator()

global_default_kettle = Kettle()
global_default_cup = Cup()

global_simulation_context = SimulationContext()
global_simulation_context.add(global_default_kettle)
global_simulation_context.add(global_default_cup)

def fill_kettle():
	global global_simulation_context
	global global_default_kettle
	
	global_default_kettle.fill_completely()
	global_simulation_context.tick()

	print("You fill the kettle with enough water for %s cups of tea!" % (global_default_kettle.water.contains,))

def turn_on_kettle():
	global global_simulation_context
	global global_default_kettle
	
	if not global_default_kettle.turned_on:
		global_default_kettle.turn_on()
		global_simulation_context.tick()
		
		print("You turn on the kettle and it starts to boil!")
	else:
		print("The kettle is already turned on, but you poke the button anyway. You feel reassured.")

def wait_until_kettle_boiled():
	global global_simulation_context
	global global_default_kettle
	
	while not global_default_kettle.is_boiled():
		global_simulation_context.tick()
	
	print("The kettle has finished boiling!")

def pour_water_into_cup():
	global global_simulation_context
	global global_default_kettle
	global global_default_cup
	
	global_default_kettle.pour_cup(global_default_cup)
	
	print("You pour some water from the kettle into the cup.")
