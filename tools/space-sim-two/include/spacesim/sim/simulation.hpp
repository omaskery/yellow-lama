#pragma once
#ifndef _INCLUDE_SIMULATION_HEADER_
#define _INCLUDE_SIMULATION_HEADER_

#include <string>

#include "timing_utils.hpp"

namespace spacesim
{
	namespace sim
	{
		class Simulation
		{
		public:
			static const unsigned int DefaultRate = 1000;
			
		public:
			Simulation();
			
			void setRates(unsigned int _rate, double _deltaTime);
			
			void load(const std::string &_filepath);
			void save(const std::string &_filepath) const;
			
			void update();
		
		private:
			double m_DeltaTime;
			unsigned int m_Rate;
			
			RateMeasurer m_ThinkMeasurer;
			RateController m_ThinkController;
			RateController m_StatsController;
		};
	}
}

#endif
