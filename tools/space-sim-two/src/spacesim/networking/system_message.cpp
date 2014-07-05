#include "spacesim/networking/system_message.hpp"

#include <stdexcept>

namespace spacesim
{
	namespace networking
	{
		std::string SystemMessage::serialise(const SystemMessage &_message)
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
		
		SystemMessage SystemMessage::deserialise(const std::string &_message)
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
	}
}
