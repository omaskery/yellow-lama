#include "spacesim/networking/system_message.hpp"

#include "utils/json.hpp"
#include <stdexcept>
#include <sstream>

namespace spacesim
{
    namespace networking
    {
        std::string SystemMessage::serialise(const SystemMessage &_message)
        {
            auto object = utils::json::Object::makeObject();
            
            object["cmd"] = _message.command();
            object["args"] = _message.parameters();
            
            return object.toStringShort();
        }
        
        SystemMessage SystemMessage::deserialise(const std::string &_message)
        {
            utils::json::Object parameters;
            std::string command = "";
            
            std::stringstream stream(_message);
            utils::json::Object object;
            
            stream >> object;
            
            if(object.hasField("cmd"))
            {
                command = object["cmd"].asString();
            }
            if(object.hasField("args"))
            {
                parameters = object["args"];
            }
            
            return SystemMessage(command, parameters);
        }
    }
}
