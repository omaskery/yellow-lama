#pragma once
#ifndef _INCLUDE_ENTITY_HEADER_
#define _INCLUDE_ENTITY_HEADER_

#include <memory>

#include "utils/json.hpp"

namespace spacesim
{
	namespace sim
	{
		class Entity
		{
		public:
			typedef std::unique_ptr<Entity> UniquePtr;
			
		public:
			Entity(const std::string &_name, const std::string &_typeName);
			inline virtual ~Entity() {}
			
			virtual void load(const utils::json::Object &_blob);
			virtual utils::json::Object save() const;
		
		private:
			std::string m_Name;
			std::string m_TypeName;
		};
	}
}

#endif
