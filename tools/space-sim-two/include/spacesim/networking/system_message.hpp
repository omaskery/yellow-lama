#pragma once
#ifndef _INCLUDE_SYSTEM_MESSAGE_HEADER_
#define _INCLUDE_SYSTEM_MESSAGE_HEADER_

#include "utils/json.hpp"

#include <string>
#include <vector>

namespace spacesim
{
    namespace networking
    {
        class SystemMessage
        {
        public:
            inline SystemMessage(const std::string &_command, const utils::json::Object &_parameters)
                : m_Command(_command), m_Parameters(_parameters) {}
            
            inline const std::string &command() const { return m_Command; }
            inline const utils::json::Object &parameters() const { return m_Parameters; }
            
            static std::string serialise(const SystemMessage &_message);
            static SystemMessage deserialise(const std::string &_message);
            
        private:
            std::string m_Command;
            utils::json::Object m_Parameters;
        };
    }
}

#endif
