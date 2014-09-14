#include "spacesim/networking/client_connection.hpp"

namespace spacesim
{
    namespace networking
    {
        ClientConnection::ClientConnection(boost::asio::ip::tcp::socket _socket, sim::Simulation &_simulation, ClientPool &_clients)
            : m_Socket(std::move(_socket)),
            m_Clients(_clients),
            m_Simulation(_simulation),
            m_ClientID(ClientPool::InvalidID)
        {
            m_Handlers["get-entity"] = [this](const SystemMessage &_message) { this->onGetEntity(_message); };
        }
        
        void ClientConnection::notify(const SystemMessage &_message)
        {
            auto message = SystemMessage::serialise(_message);
            unsigned int length = message.size();
            
            message = std::string((const char*)&length, sizeof(length)) + message;

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
            //std::cout << "[" << m_ClientID << "] got header " << m_Header << " bytes" << std::endl;
            boost::asio::async_read(m_Socket,
                boost::asio::buffer(m_Payload.data(), m_Header),
                [this, self](boost::system::error_code _error, std::size_t _length)
                {
                    if (!_error)
                    {
                        std::string raw(m_Payload.data(), m_Payload.size());
                        
                        try
                        {
                            auto message = SystemMessage::deserialise(raw);
                            handleMessage(message);
                        }
                        catch(const utils::json::Exception &_error)
                        {
                            std::cout << "[" << m_ClientID << "] failed to parse JSON:" << std::endl;
                            std::cout << "Input:" << std::endl << raw << std::endl;
                            std::cout << "Error:" << _error.what() << std::endl;
                        }
                        
                        readHeader();
                    }
                    else
                    {
                        onDisconnect();
                    }
                }
            );
        }
        
        void ClientConnection::handleMessage(const SystemMessage &_message)
        {
            //std::cout << "[" << m_ClientID << "] '" << SystemMessage::serialise(_message) << "'" << std::endl;
            
            auto found = m_Handlers.find(_message.command());
            if(found != m_Handlers.end())
            {
                found->second(_message);
            }
            else
            {
                auto args = utils::json::Object::makeObject();
                
                args["reason"] = "invalid command token";
                
                notify(SystemMessage("error", args));
            }
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
        
        void ClientConnection::onGetEntity(const SystemMessage &_message)
        {
            auto entity_list = utils::json::Object::makeList();
            auto args = _message.parameters();
            
            std::vector<sim::Entity*> entities;
            
            if(args.type() == utils::json::type::Object && args.hasField("name"))
            {
                entities = m_Simulation.subset([&](const sim::Entity &_entity){
                    return (_entity.name() == args["name"].asString());
                });
            }
            else if(args.type() == utils::json::type::Object && args.hasField("category"))
            {
                entities = m_Simulation.subset([&](const sim::Entity &_entity){
                    return (_entity.category() == args["category"].asString());
                });
            }
            else
            {
                entities = m_Simulation.subset([](const sim::Entity &){ return true; });
            }
            
            for(auto entity : entities)
            {
                entity_list.append(entity->save());
            }
            
            notify(SystemMessage("entity", entity_list));
        }
    }
}
