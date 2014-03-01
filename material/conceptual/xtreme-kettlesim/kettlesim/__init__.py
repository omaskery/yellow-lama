
import time
import sys

ROOM_TEMPERATURE = 26
BOILING_TEMPERATURE = 100
DANGER_TEMPERATURE = 45 # guesstimate at when something hurts
DRINKABLE_TEMPERATURE = 60 # according to like the NHS, seems hot!

class SimulationException(Exception):
	pass

class SimulationContext(object):
	def __init__(self):
		self.tick_count = 0
		self.objects = []
		self.running = False
		self.challenges = None
	def fetch(self, object_name):
		for obj in self.objects:
			if obj.name == object_name:
				return obj
		return None
	def horizontal_line(self):
		print("-" * 80)
	def introduction(self):
		self.horizontal_line()
		print("WELCOME TO THE XTREME KETTLE SIMULATOR 3000")
		print("THE FUTURE OF KETTLE SIMULATION IS HERE")
		self.horizontal_line()
	def goodbye(self):
		self.horizontal_line()
		print("XTREME KETTLE SIMULATOR 3000 EXITING")
		print("RETURN SOON FOR MORE KETTLE-RELATED TEXTUAL ACTION")
		self.horizontal_line()
	def error(self, description):
		self.horizontal_line()
		print("XTREME KETTLE SIMULATOR ERROR:")
		print(description)
		self.horizontal_line()
		sys.exit(-1)
	def __del__(self):
		self.goodbye()
	def should_challenge(self, name):
		if self.challenges is not None:
			return (name in self.challenges.keys())
		return False
	def tick(self):
		for obj in self.objects:
			obj.tick(self)
		self.tick_count += 1
		time.sleep(0.01)
	def add(self, obj):
		self.objects.append(obj)
	def say(self, message, with_time=True, with_newline=True):
		display = message
		if with_time:
			display = "[tick %04i] %s" % (self.tick_count, message)
		if with_newline:
			print(display)
		else:
			print(display, end='')

class SimulationObject(object):
	def __init__(self, name):
		self.name = name
	def tick(self, simulation):
		pass

class ContainerException(SimulationException):
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
		if amount > space:
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

class KettleException(SimulationException):
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
			simulation_error("Stop trying to use a broken kettle!")
			
		if self.turned_on:
			if self.water.is_empty():
				self.broken = True
				simulation_error("BOOM! Kettle set to boil with no water! Your kettle broke.")
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
			simulation_error("Splash! You overfilled the kettle, water is everywhere!")
	def fill_completely(self):
		amount = self.water.contains
		try:
			self.water.accept(self.water.capacity)
		except ContainerOverfilledException:
			if amount <= self.water.capacity:
				simulation_error("Splash! You overfilled the kettle, water is everywhere!")
			else:
				simulation_error("Splash! There's water everywhere, the kettle was already full!")
	def pour_cup(self, cup):
		if self.water.is_empty():
			simulation_error("Distressingly when you pour the kettle nothing comes out, there was no water in it!")
		
		dispensed = self.water.dispense(1)
		cup.fill(dispensed, self.temperature)

class CupException(SimulationException):
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
				simulation_error("Argh! Really hot water overfills the cup!")
			else:
				simulation_error("Argh! Water overfilfs the cup! Luckily it's not too hot.")

global_default_kettle = Kettle()
global_default_cup = Cup()

global_simulation_context = SimulationContext()
global_simulation_context.add(global_default_kettle)
global_simulation_context.add(global_default_cup)

challenges = {
	'basics': ({}, None),
	'decisions': ({}, lambda context: context.fetch("Kettle").fill_completely()),
	'repetitions': ({'boredom': True}, None)
}

def simulation_error(description):
	global global_simulation_context
	
	global_simulation_context.error(description)

def start_simulation(simulation_title):
	global global_simulation_context
	
	if simulation_title in challenges.keys():
		challenge_settings, configurator = challenges[simulation_title]
		global_simulation_context.challenges = challenge_settings
		
		global_simulation_context.introduction()
		
		if configurator is not None:
			configurator(global_simulation_context)
	else:
		simulation_error("Could not start xTreme Kettle Simulator, invalid simulation title '%s'!" % (simulation_title,))

def kettle_is_empty():
	global global_simulation_context
	global global_default_kettle
	
	result = global_default_kettle.is_empty()
	global_simulation_context.tick()
	
	state = "empty"
	if not result:
		state = "not empty"
		
	global_simulation_context.say("You check and find that the kettle is %s" % (state,))
	
	return result

def fill_kettle():
	global global_simulation_context
	global global_default_kettle
	
	global_simulation_context.say("You start pouring water into the kettle...")
	
	global_default_kettle.fill_completely()
	global_simulation_context.tick()

	global_simulation_context.say("You fill the kettle with enough water for %s cups of tea!" % (global_default_kettle.water.contains,))

def turn_on_kettle():
	global global_simulation_context
	global global_default_kettle
	
	if not global_default_kettle.turned_on:
		global_default_kettle.turn_on()
		global_simulation_context.tick()
		
		global_simulation_context.say("You turn on the kettle and it starts to boil!")
	else:
		global_simulation_context.say("The kettle is already turned on, but you poke the button anyway. You feel reassured.")

def wait_until_kettle_boiled():
	global global_simulation_context
	global global_default_kettle
	
	global_simulation_context.say("You stare vacantly into space, waiting for the kettle.")
	
	while not global_default_kettle.is_boiled():
		global_simulation_context.tick()
	
	global_simulation_context.say("The kettle has finished boiling!")

def pour_water_into_cup():
	global global_simulation_context
	global global_default_kettle
	global global_default_cup
	
	global_default_kettle.pour_cup(global_default_cup)
	
	global_simulation_context.say("You pour some water from the kettle into the cup.")
