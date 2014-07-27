#include "spacesim/sim/simulation.hpp"

#include <iostream>
#include <fstream>

namespace spacesim
{
	namespace sim
	{
		Simulation::Simulation()
			: m_DeltaTime(1.0 / DefaultRate),
			m_Rate(DefaultRate),
			m_ThinkController(Period(1.0 / m_Rate)),
			m_StatsController(Period(1.0))
		{
			setRates(m_Rate, m_DeltaTime);
		}
		
		void Simulation::setRates(unsigned int _rate, double _deltaTime)
		{
			m_Rate = _rate;
			m_DeltaTime = _deltaTime;
			
			m_ThinkController.setPeriod(Period(1.0 / m_Rate));
		}
		
		void Simulation::add(Module::UniquePtr _module)
		{
			IThink *think = dynamic_cast<IThink*>(_module.get());
			if(think != nullptr)
			{
				m_ThinkingModules.push_back(think);
			}
			m_Modules[_module->name()] = std::move(_module);
		}
		
		void Simulation::add(Entity::UniquePtr _entity)
		{
			for(auto &module : m_Modules)
			{
				module.second->onEntityCreated(*_entity.get());
			}
			m_Entities.push_back(std::move(_entity));
		}
		
		void Simulation::add(const std::string &_name, Entity::Loader _loader)
		{
			m_Loaders[_name] = _loader;
		}
		
		void Simulation::load(const std::string &_filepath)
		{
			std::ifstream input(_filepath.c_str());
			utils::json::Object blob;
			
			if(!input)
			{
				return;
			}
			
			input >> blob;
			
			for(const auto &entity : blob["entities"].asList())
			{
				std::string category = entity["category"].asString();
				
				if(m_Loaders.find(category) == m_Loaders.end())
				{
					throw std::runtime_error("no loader for entity category '" + category + "'");
				}
				
				auto loaded = m_Loaders[category](entity);
				
				add(std::move(loaded));
			}
			
			for(const auto &module : blob["modules"].asList())
			{
				std::string name = module["name"].asString();
				
				if(m_Modules.find(name) == m_Modules.end())
				{
					throw std::runtime_error("no module by name '" + name + "'");
				}
				
				m_Modules[name]->load(module);
			}
		}
		
		void Simulation::save(const std::string &_filepath) const
		{
			auto blob = utils::json::Object::makeObject();
			auto entities = utils::json::Object::makeList();
			auto modules = utils::json::Object::makeList();
			
			for(const auto &entity : m_Entities)
			{
				entities.append(entity->save());
			}
			
			for(const auto &module : m_Modules)
			{
				modules.append(module.second->save());
			}
			
			blob["entities"] = entities;
			blob["modules"] = modules;
			
			std::ofstream output(_filepath.c_str());
			output << blob << std::endl;
		}
		
		void Simulation::update()
		{
			m_ThinkController.update(
				[&]()
				{
					for(auto &module : m_ThinkingModules)
					{
						module->think();
					}
					
					m_ThinkMeasurer.count();
				}
			);
			
			m_ThinkMeasurer.update();
			
			m_StatsController.update(
				[&]()
				{
					std::cout << "stats - lps: " << m_ThinkMeasurer.eventsPerPeriod() << std::endl;
				}
			);
		}
	}
}
