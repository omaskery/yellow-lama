#include "spacesim/sim/simulation.hpp"

#include <iostream>

namespace spacesim
{
	namespace sim
	{
		Simulation::Simulation()
			: m_DeltaTime(1.0 / DefaultRate),
			m_Rate(DefaultRate),
			m_ThinkController(Period(1.0 / m_Rate)),
			m_StatsController(Period(1.0))
		{
			setRates(m_Rate, m_DeltaTime);
		}
		
		void Simulation::setRates(unsigned int _rate, double _deltaTime)
		{
			m_Rate = _rate;
			m_DeltaTime = _deltaTime;
			
			m_ThinkController.setPeriod(Period(1.0 / m_Rate));
		}
		
		void Simulation::load(const std::string &_filepath)
		{
		}
		
		void Simulation::save(const std::string &_filepath) const
		{
		}
		
		void Simulation::update()
		{
			m_ThinkController.update(
				[&]()
				{
					m_ThinkMeasurer.count();
				}
			);
			
			m_ThinkMeasurer.update();
			
			m_StatsController.update(
				[&]()
				{
					std::cout << "stats - lps: " << m_ThinkMeasurer.eventsPerPeriod() << std::endl;
				}
			);
		}
	}
}
