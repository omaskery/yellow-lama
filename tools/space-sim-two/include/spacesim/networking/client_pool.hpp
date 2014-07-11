#pragma once
#ifndef _INCLUDE_CLIENT_POOL_HEADER_
#define _INCLUDE_CLIENT_POOL_HEADER_

#include "spacesim/sim/sim_observer.hpp"

#include <boost/shared_ptr.hpp>
#include <set>

namespace spacesim
{
	namespace networking
	{
		class ClientPool
		{
		public:
			typedef unsigned int ClientID;

		public:
			const static ClientID InvalidID = 0;
			
		public:
			inline ClientPool() : m_NextFreeID(1) {}
			
			inline ClientID add(boost::shared_ptr<SimObserver> _client)
			{
				m_Clients.insert(_client);
				return m_NextFreeID ++;
			}
			
			inline void remove(boost::shared_ptr<SimObserver> _client)
			{
				m_Clients.erase(_client);
			}
		private:
			ClientID m_NextFreeID;
			std::set<boost::shared_ptr<SimObserver>> m_Clients;
		};
	}
}

#endif
