#pragma once
#ifndef _INCLUDE_SIMULATION_HEADER_
#define _INCLUDE_SIMULATION_HEADER_

#include "module.hpp"
#include "entity.hpp"
#include "ithink.hpp"
#include <string>
#include <vector>

#include "timing_utils.hpp"

namespace spacesim
{
    namespace sim
    {
        class Simulation
        {
        public:
            static const unsigned int DefaultRate = 100000;
            
        public:
            Simulation();
            
            void setRates(unsigned int _rate, double _deltaTime);
            
            void add(Module::UniquePtr _module);
            void add(Entity::UniquePtr _entity);
            void add(const std::string &_name, Entity::Loader _loader);
            
            void load(const std::string &_filepath);
            void save(const std::string &_filepath) const;
            
            void update();
            
            std::vector<Entity*> subset(std::function<bool(const Entity&)> _filter);
        
        private:
            double m_DeltaTime;
            unsigned int m_Rate;
            
            RateMeasurer m_ThinkMeasurer;
            RateController m_ThinkController;
            RateController m_StatsController;
            
            std::vector<IThink*> m_ThinkingModules;
            std::vector<Entity::UniquePtr> m_Entities;
            std::map<std::string, Module::UniquePtr> m_Modules;
            
            std::map<std::string, Entity::Loader> m_Loaders;
        };
    }
}

#endif
