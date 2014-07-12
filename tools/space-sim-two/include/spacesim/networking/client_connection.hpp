#pragma once
#ifndef _INCLUDE_CLIENT_CONNECTION_HEADER_
#define _INCLUDE_CLIENT_CONNECTION_HEADER_

#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/asio.hpp>
#include <boost/bind.hpp>

#include <vector>
#include <list>

#include "spacesim/sim/sim_observer.hpp"
#include "spacesim/sim/simulation.hpp"
#include "client_pool.hpp"

namespace spacesim
{
	namespace networking
	{
		class ClientConnection
		  : public boost::enable_shared_from_this<ClientConnection>, public SimObserver
		{	
		public:
			typedef boost::shared_ptr<ClientConnection> shared_ptr;

		public:
			ClientConnection(boost::asio::ip::tcp::socket _socket, sim::Simulation &_simulation, ClientPool &_clients);

			void notify(const SystemMessage &_message) override;
			void start();

		private:
			void pumpTransmit();
			void readHeader();
			void readPayload();
			void handleWrite(const boost::system::error_code& _error, size_t _bytes_transferred);
			void onDisconnect();

		private:
			boost::asio::ip::tcp::socket m_Socket;
			ClientPool &m_Clients;
			unsigned int m_Header;
			std::vector<char> m_Payload;
			sim::Simulation &m_Simulation;
			ClientPool::ClientID m_ClientID;
			std::list<std::string> m_Messages;
		};
	}
}

#endif
