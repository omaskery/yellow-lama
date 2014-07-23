#include "spacesim/sim/entity.hpp"

namespace spacesim
{
	namespace sim
	{
		Entity::Entity(const std::string &_name, const std::string &_category)
			: m_Name(_name), m_Category(_category)
		{
		}
		
		void Entity::load(const utils::json::Object &_blob)
		{
			m_Name = _blob["name"].asString();
			m_Category = _blob["category"].asString();
		}
		
		utils::json::Object Entity::save() const
		{
			using utils::json::Object;
			
			auto blob = Object::makeObject();
			
			blob["name"] = Object(m_Name);
			blob["category"] = Object(m_Category);
			
			return blob;
		}
	}
}
