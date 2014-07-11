#pragma once
#ifndef _INCLUDE_SIMULATION_HEADER_
#define _INCLUDE_SIMULATION_HEADER_

#include <string>

namespace spacesim
{
	namespace sim
	{
		class Simulation
		{
		public:
			Simulation();
			
			void load(const std::string &_filepath);
			void save(const std::string &_filepath);
			
			void update();
		
		private:
		};
	}
}

#endif
