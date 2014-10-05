
#include "spacesim/sim/radio_module.hpp"

namespace spacesim
{
    namespace sim
    {
        void RadioEmission::think(double _dt)
        {
            m_Radius += RadiusIncrease * _dt;
            m_Position += m_Velocity * _dt;
        }
        
        float RadioEmission::pathLoss() const { 
            const double distance = (m_Position - m_Origin).magnitude();
            const double constant = 147.55;
            
            return 20.0 * log10(distance) + 20 * log10(m_Frequency) - constant;
        }
        
        void RadioModule::onEntityCreated(Entity &_entity)
        {
        }
        
        void RadioModule::onEntityDestroyed(Entity &_entity)
        {
        }
        
        void RadioModule::load(const utils::json::Object &_blob)
        {
        }
        
        utils::json::Object RadioModule::save() const
        {
            auto blob = Module::save();
            
            return blob;
        }
        
        void RadioModule::think(double _dt)
        {
        }
    }
}
