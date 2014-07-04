
#include <iostream>
#include <memory>
#include <string>
#include <list>
#include <set>

#include <boost/bind.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/enable_shared_from_this.hpp>
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

class SystemMessage
{
public:
	typedef std::unique_ptr<SystemMessage> unique_ptr;
	
public:
	SystemMessage(const std::string &_command, const std::vector<std::string> &_parameters)
		: m_Command(_command), m_Parameters(_parameters) {}
	
	inline const std::string &command() const { return m_Command; }
	inline const std::vector<std::string> &parameters() const { return m_Parameters; }
	inline auto size() const -> decltype(parameters().size()) { return m_Parameters.size(); }
	inline std::string parameter(unsigned int _index) const { return m_Parameters[_index]; }
	
	static std::string serialise(const SystemMessage &_message)
	{
		std::string result = "#" + _message.command() + ":";
		for(unsigned int index = 0; index < _message.size(); index ++)
		{
			if(index != 0) result += ",";
			result += _message.parameter(index);
		}
		result += "\r\n";
		return result;
	}
	
	static SystemMessage deserialise(const std::string &_message)
	{
		std::vector<std::string> parameters;
		std::string command = "";
		
		if(_message[0] != '#') throw std::runtime_error("expected mark at start of message");
		
		auto command_end = _message.find(':');
		
		if(command_end != std::string::npos)
		{
			command = _message.substr(1, command_end - 1);
			
			auto last_position = command_end + 1;
			while(true)
			{
				auto parameter_end = _message.find(',', last_position);
				auto length = parameter_end - last_position;
				
				if(parameter_end != std::string::npos)
				{
					if(length > 0)
					{
						parameters.push_back(_message.substr(last_position, length));
					}
					last_position = parameter_end + 1;
				}
				else
				{
					if(length > 0)
					{
						parameters.push_back(_message.substr(last_position));
					}
					break;
				}
			}
		}
		else
		{
			command = _message.substr(1);
		}
		
		return SystemMessage(command, parameters);
	}
	
private:
	std::string m_Command;
	std::vector<std::string> m_Parameters;
};

class SimObserver
{
public:
	virtual void notify(const SystemMessage &_message) = 0;
};

class ClientPool
{
public:
	typedef unsigned int ClientID;

public:
	const static ClientID InvalidID = 0;
	
public:
	inline ClientPool() : m_NextFreeID(1) {}
	
	ClientID add(boost::shared_ptr<SimObserver> _client)
	{
		m_Clients.insert(_client);
		return m_NextFreeID ++;
	}
	
	void remove(boost::shared_ptr<SimObserver> _client)
	{
		m_Clients.erase(_client);
	}
private:
	ClientID m_NextFreeID;
	std::set<boost::shared_ptr<SimObserver>> m_Clients;
};

class ClientConnection
  : public boost::enable_shared_from_this<ClientConnection>, public SimObserver
{
public:
	typedef boost::shared_ptr<ClientConnection> shared_ptr;

public:
	ClientConnection(tcp::socket _socket, ClientPool &_clients)
		: m_Socket(std::move(_socket)), m_Clients(_clients), m_ClientID(ClientPool::InvalidID)
	{
	}

	void notify(const SystemMessage &_message) override
	{
		auto message = SystemMessage::serialise(_message);

		m_Messages.push_back(message);

		if(m_Messages.size() == 1)
		{
			pumpTransmit();
		}
	}

	void start()
	{
		m_ClientID = m_Clients.add(shared_from_this());
		
		std::cout << "[" << m_ClientID << "] connected" << std::endl;
		
		readHeader();
		
		notify(SystemMessage("test", {"one", "two", "three"}));
	}

private:
	void pumpTransmit()
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
	
	void readHeader()
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
	
	void readPayload()
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

	void handleWrite(const boost::system::error_code& _error, size_t _bytes_transferred)
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
	
	void onDisconnect()
	{
		std::cout << "[" << m_ClientID << "] disconnected" << std::endl;
		m_Clients.remove(shared_from_this());
	}

	tcp::socket m_Socket;
	ClientPool &m_Clients;
	unsigned int m_Header;
	std::vector<char> m_Payload;
	ClientPool::ClientID m_ClientID;
	std::list<std::string> m_Messages;
};

class SimServer
{
public:
	SimServer(boost::asio::io_service& _service, int _port)
		: m_Socket(_service), m_Acceptor(_service, tcp::endpoint(tcp::v4(), _port))
	{
		startAccept();
	}

private:
	void startAccept()
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

	ClientPool m_Clients;
	tcp::socket m_Socket;
	tcp::acceptor m_Acceptor;
};

int main()
{
  try
  {
    boost::asio::io_service io_service;
    SimServer server(io_service, 40000);
    
    while(true)
    {
		io_service.poll();
	}
  }
  catch (std::exception& e)
  {
    std::cerr << e.what() << std::endl;
  }

  return 0;
}
