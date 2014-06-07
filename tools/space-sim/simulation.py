
import datetime

import sim_module
import entities
import json

import gravity_module

def now():
	return datetime.datetime.now()

def now_plus(seconds):
	return now() + datetime.timedelta(seconds=seconds)

class Simulation(object):
	
	def __init__(self):
		self.running = True
		
		self.sim_time = 0
		self.sim_rate = 200
		self.sim_dt = 1.0 / self.sim_rate
		#self.sim_dt = 100
		self.sim_tick = now_plus(1.0 / self.sim_rate)
		
		self.ticks = 0
		self.tick_delta = 0
		
		self.stat_period = 60
		self.stat_tick = now_plus(self.stat_period)
		
		self.next_uid = 1
		
		self.entity_factories = {}
		
		self.entities = {}
		self.thinking = []
		
		self.modules = {}
		self.thinking_modules = []
		
		self.register_module(gravity_module.Gravity(self))
	
	def allocate_uid(self):
		uid = self.next_uid
		self.next_uid += 1
		return uid
	
	def register_entity_category(self, category_uid, entity_class):
		self.entity_factories[category_uid] = entities.EntityFactory(category_uid, entity_class)
	
	def register_module(self, module):
		if module.name in self.modules.keys():
			return False
				
		self.modules[module.name] = module
		
		if module.should_think():
			self.thinking_modules.append(module)
	
	def unregister_module(self, module):
		if module.name in self.modules.keys():
			del self.modules[module.name]
		
		if module.should_think():
			self.thinking_modules.remove(module)
	
	def add_entity(self, entity):
		if entity.uid in self.entities.keys():
			return False
			
		self.entities[entity.uid] = entity
		
		if entity.should_think():
			self.thinking.append(entity)
		
		for module in self.modules.values():
			module.on_new_entity(entity)
		
		return True
		
	def remove_entity(self, entity):
		if entity.uid in self.entities.keys():
			del self.entities[entity.uid]
		
		if entity.should_think():
			self.thinking.remove(entity)
		
		for module in self.modules.values():
			module.on_entity_removed(entity)
	
	def save(self, filepath):
		absorb_errors = False
		
		handle = open(filepath, 'w')
		for module in self.modules.values():
			try:
				blob = module.save()
				blob_json = json.dumps(blob)
				handle.write("module:%s\r\n" % blob_json)
			except:
				print "[space-sim] error saving module"
				if not absorb_errors:
					raise
		for entity in self.entities.values():
			try:
				blob = entity.save()
				blob_json = json.dumps(blob)
				handle.write("entity:%s\r\n" % blob_json)
			except:
				print "[space-sim] error saving entity"
				if not absorb_errors:
					raise
	
	def load(self, filepath):
		absorb_errors = False
		
		handle = open(filepath, 'r')
		for line in handle.readlines():
			if not line: continue
			try:
				seperator = line.find(":")
				if seperator == -1:
					raise Exception("expected ':' seperator")
				
				line_type = line[:seperator]
				blob_json = line[seperator+1:]
				
				blob = json.loads(blob_json)
				
				if line_type == 'module':
					module_name = blob['module-name']
					module = self.modules[module_name]
					module.load(blob)
				elif line_type == 'entity':
					category_uid = blob['category_uid']
					factory = self.entity_factories[category_uid]
					entity = factory.load(blob, self)
					
					self.add_entity(entity)
			except:
				print "[space-sim] error loading entity"
				if not absorb_errors:
					raise
	
	def stop(self):
		self.running = False
	
	def update(self):
		if now() >= self.sim_tick:
			self.sim_tick += datetime.timedelta(seconds = 1.0 / self.sim_rate)
			self.sim_time += self.sim_dt
			
			self.think(self.sim_dt)
			
			self.ticks += 1
			self.tick_delta += 1
			
		if now() >= self.stat_tick:
			self.stat_tick += datetime.timedelta(seconds = self.stat_period)
			
			print "[sim-server] %s ticks/s %s entities" % (self.tick_delta / self.stat_period, len(self.entities))
			self.tick_delta = 0
	
	def think(self, dt):
		for module in self.thinking_modules:
			module.think(dt)
		for entity in self.thinking:
			entity.think(dt)
