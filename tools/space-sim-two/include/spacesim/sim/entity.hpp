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
			typedef std::function<Entity::UniquePtr(const utils::json::Object &_blob)> Loader;
			
		public:
			Entity(const std::string &_name, const std::string &_category);
			inline virtual ~Entity() {}
			
			inline const std::string &name() const { return m_Name; }
			inline const std::string &category() const { return m_Category; }
			
			virtual void load(const utils::json::Object &_blob);
			virtual utils::json::Object save() const;
		
		private:
			std::string m_Name;
			std::string m_Category;
		};
	}
}

#endif
