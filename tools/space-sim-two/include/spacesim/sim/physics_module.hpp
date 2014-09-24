#pragma once
#ifndef _INCLUDE_PHYSICS_MODULE_HEADER_
#define _INCLUDE_PHYSICS_MODULE_HEADER_

#include "utils/vector.hpp"
#include "module.hpp"
#include "ithink.hpp"

namespace spacesim
{
    namespace sim
    {
        typedef double PhysicsUnit;
        
        typedef utils::Vector<PhysicsUnit, 3> PhysicsVector;
        typedef PhysicsVector Position;
        typedef PhysicsVector Velocity;
        typedef PhysicsVector Force;
        typedef PhysicsUnit Radius;
        typedef PhysicsUnit Mass;
        
        inline PhysicsVector VectorFromJson(utils::json::Object _blob)
        {
            return PhysicsVector(
                _blob[0].asDouble(),
                _blob[1].asDouble(),
                _blob[2].asDouble()
            );
        }
        
        inline utils::json::Object JsonFromVector(const PhysicsVector &_vector)
        {
            auto blob = utils::json::Object::makeList();
            
            blob.append(_vector.x());
            blob.append(_vector.y());
            blob.append(_vector.z());
            
            return blob;
        }
        
        class PhysicalBody : public Entity
        {
        public:
            typedef std::unique_ptr<PhysicalBody> UniquePtr;
            
        public:
            inline PhysicalBody(const std::string &_name) : Entity(_name, "physical-entity"), m_Fixed(false) {}
            
            inline void accelerate(const Force &_force, double _dt) { if(!m_Fixed) m_Velocity += (_force / m_Mass) * _dt; }
            void updatePhysics(double _dt);
            
            inline void setFixed(bool _fixed) { m_Fixed = _fixed; }
            inline void setMass(Mass _mass) { m_Mass = _mass; }
            inline void setRadius(Radius _radius) { m_Radius = _radius; }
            inline void setVelocity(const Velocity &_velocity) { m_Velocity = _velocity; }
            inline void setPosition(const Position &_position) { m_Position = _position; }
            
            inline bool fixed() const { return m_Fixed; }
            inline Mass mass() const { return m_Mass; }
            inline Radius radius() const { return m_Radius; }
            inline Velocity velocity() const { return m_Velocity; }
            inline Position position() const { return m_Position; }
            
            void load(const utils::json::Object &_blob) override;
            utils::json::Object save() const override;
            
        private:
            Mass m_Mass;
            bool m_Fixed;
            Radius m_Radius;
            Velocity m_Velocity;
            Position m_Position;
        };
        
        class PhysicsModule : public Module, public IThink
        {
        public:
            inline PhysicsModule() : Module("physics-module") {}
            
            void onEntityCreated(Entity &_entity) override;
            void onEntityDestroyed(Entity &_entity) override;
            
            void load(const utils::json::Object &_blob) override;
            utils::json::Object save() const override;
            
            void think(double _dt) override;
        
        private:
            void applyGravity(PhysicalBody *_a, PhysicalBody *_b, double _dt);
        
        private:
            std::vector<PhysicalBody*> m_Entities;
        };
    }
}

#endif
