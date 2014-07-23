#include "spacesim/sim/module.hpp"

namespace spacesim
{
	namespace sim
	{
		void Module::load(const utils::json::Object &_blob)
		{
			m_Name = _blob["name"].asString();
		}
		
		utils::json::Object Module::save() const
		{
			auto blob = utils::json::Object::makeObject();
			
			blob["name"] = m_Name;
			
			return blob;
		}
	}
}
