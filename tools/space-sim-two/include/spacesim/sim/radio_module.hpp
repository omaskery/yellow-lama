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
            const PhysicsUnit RadiusIncrease = SpeedOfLight;
        
        public:
            inline RadioEmission(const Position &_origin, const PhysicsVector &_direction, float _power, float _radius, double _frequency)
                : m_Origin(_origin), m_Frequency(_frequency), m_SourcePower(_power),
                m_Radius(_radius), m_Velocity(_direction * SpeedOfLight), m_Position(_origin)
            {
            }
            
            void think(double _dt);
            
            inline float power() const { return m_SourcePower - pathLoss(); }
            inline float sourcePower() const { return m_SourcePower; }
            
            inline Radius radius() const { return m_Radius; }
            inline Velocity velocity() const { return m_Velocity; }
            inline Position position() const { return m_Position; }
        
        private:
            float pathLoss() const;
        
        private:
            Position m_Origin;
            double m_Frequency;
            float m_SourcePower;
            
            Radius m_Radius;
            Velocity m_Velocity;
            Position m_Position;
        };
        
        class RadioTransceiver // derive from some kind of "Ship Component" base class?
        {
        public:
        
        private:
            //const Position &m_Position; // get position from parent or something?
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
