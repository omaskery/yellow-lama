#pragma once
#ifndef _INCLUDE_RADIO_MODULE_HEADER_
#define _INCLUDE_RADIO_MODULE_HEADER_

#include "physics_module.hpp"

namespace spacesim
{
	namespace sim
	{
		class RadioEmission
		{
		public:
			const PhysicsUnit SpeedOfLight = 3E8;
		
		public:
			inline RadioEmission(const Position &_origin, const PhysicsVector &_direction, float _power, float _radius)
				: m_Power(_power), m_SourcePower(_power), m_Radius(_radius),
				m_Position(_origin), m_Velocity(_direction * SpeedOfLight)
			{ // antenna gain, direction (EIRB)
			}
			
			void think(double _dt);
			
			inline float power() const { return m_Power; }
			inline float sourcePower() const { return m_SourcePower; }
			
			inline Radius radius() const { return m_Radius; }
			inline Velocity velocity() const { return m_Velocity; }
			inline Position position() const { return m_Position; }
		
		private:
			float m_Power;
			float m_SourcePower;
			
			Radius m_Radius;
			Velocity m_Velocity;
			Position m_Position;
		};
		
		class RadioModule : public Module, public IThink
        {
        public:
            inline RadioModule() : Module("radio-module") {}
            
            void onEntityCreated(Entity &_entity) override;
            void onEntityDestroyed(Entity &_entity) override;
            
            void load(const utils::json::Object &_blob) override;
            utils::json::Object save() const override;
            
            void think(double _dt) override;
        
        private:
            std::vector<PhysicalBody*> m_Entities;
            std::vector<RadioEmission> m_Emissions;
        };
	}
}

#endif
