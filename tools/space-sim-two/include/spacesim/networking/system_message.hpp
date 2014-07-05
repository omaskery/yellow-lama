#pragma once
#ifndef _INCLUDE_SYSTEM_MESSAGE_HEADER_
#define _INCLUDE_SYSTEM_MESSAGE_HEADER_

#include <string>
#include <vector>

namespace spacesim
{
	namespace networking
	{
		class SystemMessage
		{
		public:
			inline SystemMessage(const std::string &_command, const std::vector<std::string> &_parameters)
				: m_Command(_command), m_Parameters(_parameters) {}
			
			inline const std::string &command() const { return m_Command; }
			inline const std::vector<std::string> &parameters() const { return m_Parameters; }
			inline auto size() const -> decltype(parameters().size()) { return m_Parameters.size(); }
			inline std::string parameter(unsigned int _index) const { return m_Parameters[_index]; }
			
			static std::string serialise(const SystemMessage &_message);
			static SystemMessage deserialise(const std::string &_message);
			
		private:
			std::string m_Command;
			std::vector<std::string> m_Parameters;
		};
	}
}

#endif
