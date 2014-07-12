#include "spacesim/sim/entity.hpp"

namespace spacesim
{
	namespace sim
	{
		Entity::Entity(const std::string &_name, const std::string &_typeName)
			: m_Name(_name), m_TypeName(_typeName)
		{
		}
		
		void Entity::load(const utils::json::Object &_blob)
		{
			m_Name = _blob["name"].asString();
			m_TypeName = _blob["type"].asString();
		}
		
		utils::json::Object Entity::save() const
		{
			using utils::json::Object;
			
			auto blob = Object::makeObject();
			
			blob["name"] = Object(m_Name);
			blob["type"] = Object(m_TypeName);
			
			return blob;
		}
	}
}
