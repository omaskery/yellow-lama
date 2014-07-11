#pragma once
#ifndef _INCLUDE_SIM_SERVER_HEADER_
#define _INCLUDE_SIM_SERVER_HEADER_

#include <boost/shared_ptr.hpp>
#include <boost/asio.hpp>

#include "client_connection.hpp"
#include "client_pool.hpp"

namespace spacesim
{
	namespace networking
	{
		class SimServer
		{
		public:
			SimServer(boost::asio::io_service& _service, int _port);

		private:
			void startAccept();

		private:
			ClientPool m_Clients;
			boost::asio::ip::tcp::socket m_Socket;
			boost::asio::ip::tcp::acceptor m_Acceptor;
		};
	}
}

#endif
