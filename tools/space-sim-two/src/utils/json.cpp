#include "utils/json.hpp"

namespace utils
{
	namespace json
	{
		void Object::serialise(std::ostream &_stream, int _indent) const
		{
			const std::string Indent = "  ";
			
			auto indent = [&](int _amount){
				for(int i = 0; i < _amount; i++)
				{
					_stream << Indent;
				}
			};
			
			auto writeValue = [&](){
				indent(_indent);
				_stream << m_Value;
			};
			
			switch(m_Type)
			{
			case type::Integer:
				{
					writeValue();
				} break;
			case type::Decimal:
				{
					writeValue();
				} break;
			case type::String:
				{
					writeValue();
				} break;
			case type::Boolean:
				{
					writeValue();
				} break;
			case type::List:
				{
					indent(_indent); _stream << "[" << std::endl;
					
					for(int index = 0; index < m_Elements.size(); index++)
					{
						if(index > 0) _stream << ",";
						_stream << std::endl;
						
						m_Elements[index].serialise(_stream, _indent + 1);
					}
					
					indent(_indent); _stream << "]";
				} break;
			case type::Object:
				{
					indent(_indent); _stream << "{" << std::endl;
					
					for(auto iterator = m_Members.begin(); iterator != m_Members.end(); iterator++)
					{
						if(iterator != m_Members.begin()) _stream << ",";
						_stream << std::endl;
						
						iterator->second.serialise(_stream, _indent + 1);
					}
					
					indent(_indent); _stream << "}";
				} break;
			default:
				{
					// can't do anything here :x
				} break;
			}
		}
		
		void Object::deserialise(std::istream &_stream)
		{
			
		}
	}
}
