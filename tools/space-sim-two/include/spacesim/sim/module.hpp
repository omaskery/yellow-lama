#pragma once
#ifndef _INCLUDE_MODULE_HEADER_
#define _INCLUDE_MODULE_HEADER_

#include "entity.hpp"

namespace spacesim
{
	namespace sim
	{
		class Module
		{
		public:
			typedef std::unique_ptr<Module> UniquePtr;
			
		public:
			inline Module(const std::string &_name) : m_Name(_name) {}
			inline virtual ~Module() {}
			
			inline const std::string &name() const { return m_Name; }
			
			inline virtual void onEntityCreated(Entity &_entity) {}
			inline virtual void onEntityDestroyed(Entity &_entity) {}
			
			virtual void load(const utils::json::Object &_blob);
			virtual utils::json::Object save() const;
			
		private:
			std::string m_Name;
		};
	}
}

#endif
