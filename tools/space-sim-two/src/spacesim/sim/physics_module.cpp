#include "spacesim/sim/physics_module.hpp"

#include <algorithm>

namespace spacesim
{
	namespace sim
	{
		void PhysicalBody::updatePhysics()
		{
			m_Position += m_Velocity;
		}
		
		void PhysicalBody::load(const utils::json::Object &_blob)
		{
			Entity::load(_blob);
			
			m_Mass = _blob["physical"]["mass"].asDouble();
			m_Fixed = _blob["physical"]["fixed"].asBoolean();
			m_Radius = _blob["physical"]["radius"].asDouble();
			m_Velocity = VectorFromJson(_blob["physical"]["velocity"]);
			m_Position = VectorFromJson(_blob["physical"]["position"]);
		}
		
		utils::json::Object PhysicalBody::save() const
		{
			auto blob = Entity::save();
			
			blob["physical"] = utils::json::Object::makeObject();
			
			blob["physical"]["mass"] = m_Mass;
			blob["physical"]["fixed"] = m_Fixed;
			blob["physical"]["radius"] = m_Radius;
			blob["physical"]["velocity"] = JsonFromVector(m_Velocity);
			blob["physical"]["position"] = JsonFromVector(m_Position);
			
			return blob;
		}
		
		void PhysicsModule::onEntityCreated(Entity &_entity)
		{
			PhysicalBody *body = dynamic_cast<PhysicalBody*>(&_entity);
			
			if(body != nullptr)
			{
				m_Entities.push_back(body);
			}
		}
		
		void PhysicsModule::onEntityDestroyed(Entity &_entity)
		{
			for(auto iter = m_Entities.begin(); iter != m_Entities.end(); iter++)
			{
				if(*iter == &_entity)
				{
					m_Entities.erase(iter);
					break;
				}
			}
		}
		
		void PhysicsModule::load(const utils::json::Object &_blob)
		{
			
		}
		
		utils::json::Object PhysicsModule::save() const
		{
			auto blob = utils::json::Object::makeObject();
			
			return blob;
		}
		
		void PhysicsModule::think()
		{
			for(unsigned int index = 0; index < m_Entities.size(); index++)
			{
				for(unsigned int inner_index = index+1; inner_index < m_Entities.size(); inner_index++)
				{
					applyGravity(m_Entities[index], m_Entities[inner_index]);
				}
			}
			
			for(auto entity : m_Entities)
			{
				entity->updatePhysics();
			}
		}
		
		void PhysicsModule::applyGravity(PhysicalBody *_a, PhysicalBody *_b)
		{
			const PhysicsUnit G = 6.67E-11;
			// F = Gm1m2/r^2
			auto delta = (_a->position() - _b->position());
			auto force = (G * _a->mass() * _b->mass()) / std::max(delta.magnitude(), 1E-3);
			
			auto forceVector = delta.normalised() * force;
			
			_a->accelerate(forceVector);
			_b->accelerate(forceVector * -1);
		}
	}
}
