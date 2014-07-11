#include "spacesim/networking/sim_server.hpp"

namespace spacesim
{
	namespace networking
	{
		SimServer::SimServer(boost::asio::io_service& _service, int _port)
			: m_Socket(_service), m_Acceptor(_service, boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), _port))
		{
			startAccept();
		}
		
		void SimServer::startAccept()
		{
			m_Acceptor.async_accept(m_Socket,
				[&](const boost::system::error_code &_error)
				{
					if(!_error)
					{
						boost::shared_ptr<ClientConnection>(new ClientConnection(std::move(m_Socket), m_Clients))->start();
					}
					
					startAccept();
				}
			);
		}
	}
}
