#pragma once
#ifndef _INCLUDE_SIM_OBSERVER_HEADER_
#define _INCLUDE_SIM_OBSERVER_HEADER_

#include "spacesim/networking/system_message.hpp"

namespace spacesim
{
	namespace networking
	{
		class SimObserver
		{
		public:
			virtual void notify(const SystemMessage &_message) = 0;
		};
	}
}

#endif
