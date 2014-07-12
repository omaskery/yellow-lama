#pragma once
#ifndef _INCLUDE_TIMING_UTILS_HEADER_
#define _INCLUDE_TIMING_UTILS_HEADER_

#include <functional>
#include <chrono>

namespace spacesim
{
	namespace sim
	{
		typedef std::chrono::steady_clock Clock;
		typedef std::chrono::duration<double> Period;
		typedef std::chrono::time_point<Clock, Period> Instant;
		
		class Timer
		{
		public:
			inline Timer() : m_Start(Clock::now()) {}
			
			inline Period elapsed() const { return (Clock::now() - m_Start); }
			inline bool exceeds(const Period &_period) const { return (elapsed() > _period); }
			
			inline void reset() { m_Start = Clock::now(); }
			inline void advance(const Period &_period) { m_Start += _period; }
			
		private:
			Instant m_Start;
		};
		
		class RateController
		{
		public:
			inline RateController(Period _period) : m_Next(Clock::now()), m_Period(_period) {}
			
			inline void update(std::function<void()> _handler)
			{
				if(Clock::now() > m_Next)
				{
					m_Next += m_Period;
					_handler();
				}
			}
			
			inline void setPeriod(Period _period) { m_Period = _period; }
		
		private:
			Instant m_Next;
			Period m_Period;
		};
		
		class RateMeasurer
		{
		public:
			inline RateMeasurer(Period _period = Period(1.0)) : m_Controller(_period), m_Events(0), m_EventsPerPeriod(0.0) {}
			
			inline void count() { m_Events++; }
			inline unsigned int eventsPerPeriod() const { return m_EventsPerPeriod; }
			
			inline void update()
			{
				m_Controller.update(
					[&]()
					{
						m_EventsPerPeriod = m_Events;
						m_Events = 0;
					}
				);
			}
			
		private:
			unsigned int m_Events;
			unsigned int m_EventsPerPeriod;
			RateController m_Controller;
		};
	}
}

#endif
