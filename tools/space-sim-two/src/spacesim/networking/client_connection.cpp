#include "spacesim/networking/client_connection.hpp"

namespace spacesim
{
	namespace networking
	{
		ClientConnection::ClientConnection(boost::asio::ip::tcp::socket _socket, ClientPool &_clients)
			: m_Socket(std::move(_socket)), m_Clients(_clients), m_ClientID(ClientPool::InvalidID)
		{
		}
		
		void ClientConnection::notify(const SystemMessage &_message)
		{
			auto message = SystemMessage::serialise(_message);

			m_Messages.push_back(message);

			if(m_Messages.size() == 1)
			{
				pumpTransmit();
			}
		}
		
		void ClientConnection::start()
		{
			m_ClientID = m_Clients.add(shared_from_this());
			
			std::cout << "[" << m_ClientID << "] connected" << std::endl;
			
			readHeader();
			
			notify(SystemMessage("test", {"one", "two", "three"}));
		}
		
		void ClientConnection::pumpTransmit()
		{
			if(m_Messages.size() > 0)
			{
				boost::asio::async_write(m_Socket, boost::asio::buffer(m_Messages.front()),
					boost::bind(&ClientConnection::handleWrite, shared_from_this(),
					boost::asio::placeholders::error,
					boost::asio::placeholders::bytes_transferred)
				);
			}
		}
		
		void ClientConnection::readHeader()
		{
			auto self(shared_from_this());
			boost::asio::async_read(m_Socket,
				boost::asio::buffer(reinterpret_cast<char*>(&m_Header), sizeof(m_Header)),
				[this, self](boost::system::error_code _error, std::size_t _length)
				{
					if (!_error)
					{
						readPayload();
					}
					else
					{
						onDisconnect();
					}
				}
			);
		}
		
		void ClientConnection::readPayload()
		{
			auto self(shared_from_this());
			m_Payload.resize(m_Header);
			boost::asio::async_read(m_Socket,
				boost::asio::buffer(m_Payload.data(), m_Header),
				[this, self](boost::system::error_code _error, std::size_t _length)
				{
					if (!_error)
					{
						std::string message(m_Payload.data(), m_Payload.size());
						
						std::cout << "[" << m_ClientID << "] '" << message << "'" << std::endl;
						
						readHeader();
					}
					else
					{
						onDisconnect();
					}
				}
			);
		}
		
		void ClientConnection::handleWrite(const boost::system::error_code& _error, size_t _bytes_transferred)
		{
			if(!_error)
			{
				m_Messages.pop_front();
				pumpTransmit();
			}
			else
			{
				onDisconnect();
			}
		}
		
		void ClientConnection::onDisconnect()
		{
			std::cout << "[" << m_ClientID << "] disconnected" << std::endl;
			m_Clients.remove(shared_from_this());
		}
	}
}
