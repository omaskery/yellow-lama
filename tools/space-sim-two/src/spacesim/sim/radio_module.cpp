
#include "spacesim/sim/radio_module.hpp"

namespace spacesim
{
	namespace sim
	{
		void RadioEmission::think(double _dt)
		{
		}
		
		void RadioModule::onEntityCreated(Entity &_entity)
		{
		}
		
		void RadioModule::onEntityDestroyed(Entity &_entity)
		{
		}
		
		void RadioModule::load(const utils::json::Object &_blob)
		{
		}
		
		utils::json::Object RadioModule::save() const
		{
			auto blob = Module::save();
			
			return blob;
		}
		
		void RadioModule::think(double _dt)
		{
		}
	}
}
