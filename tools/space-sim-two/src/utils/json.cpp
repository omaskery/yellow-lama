#include "utils/json.hpp"

namespace utils
{
	namespace json
	{
		
		Parser::Parser(std::istream &_stream)
			: m_Stream(_stream), m_Line(1), m_Char(1)
		{
		}
		
		Object Parser::parse()
		{
			Object root = Object::makeObject();
			
			parseObject(root);
			
			return root;
		}
		
		void Parser::parseValue(Object &_value)
		{
			skipWhitespace();
			
			const char Next = peek();
			
			if(Next == '{')
			{
				_value = Object::makeObject();
				parseObject(_value);
			}
			else if(Next == '[')
			{
				_value = Object::makeList();
				parseList(_value);
			}
			else if(Next == 't' || Next == 'f')
			{
				parseBool(_value);
			}
			else if(Next == '"')
			{
				parseString(_value);
			}
			else if(isdigit(Next))
			{
				parseNumeric(_value);
			}
			else
			{
				error(std::string("unexpected character '") + Next + "'");
			}
		}
		
		void Parser::parseObject(Object &_object)
		{
			expect("{");
			skipWhitespace();
			
			bool first = true;
			
			while(peek() != '}')
			{
				if(!first)
					expect(",");
				
				first = false;
				
				Object fieldname;
				parseString(fieldname);
				
				expect(":");
				
				Object value;
				parseValue(value);
				
				_object.setField(fieldname.asString(), value);
				
				skipWhitespace();
			}
			
			expect("}");
		}
		
		void Parser::parseString(Object &_string)
		{
			expect("\"");
			skipWhitespace();
			
			std::string contents = "";
			
			while(peek() != '"')
			{
				contents += get();
				skipWhitespace();
			}
			
			_string = Object(contents);
			
			expect("\"");
		}
		
		void Parser::parseNumeric(Object &_numeric)
		{
			std::string contents = "";
			bool seperator = false;
			
			skipWhitespace();
			
			while(isdigit(peek()) || (peek() == '.' && !seperator))
			{
				if(peek() == '.')
					seperator = false;
					
				contents += get();
			}
			
			if(seperator)
			{
				_numeric = Object(contents, type::Decimal);
			}
			else
			{
				_numeric = Object(contents, type::Integer);
			}
		}
		
		void Parser::parseList(Object &_list)
		{
			expect("[");
			skipWhitespace();
			
			while(peek() != ']')
			{
				if(_list.size() > 0)
					expect(",");
				
				Object value;
				parseValue(value);
				_list.append(value);
				
				skipWhitespace();
			}
			
			expect("]");
		}
		
		void Parser::parseBool(Object &_boolean)
		{
			if(peek() == 't')
			{
				expect("true");
				_boolean = Object(true);
			}
			else
			{
				expect("false");
				_boolean = Object(false);
			}
		}
		
		void Parser::expect(const std::string &_expected)
		{
			skipWhitespace();
			
			std::cout << "expecting '" << _expected << "'" << std::endl;
			
			for(char letter : _expected)
			{
				if(get() != letter)
				{
					error("expected string '" + _expected + "'");
				}
			}
		}
		
		void Parser::skipWhitespace()
		{
			int skipped = 0;
			while(isspace(peek()))
			{
				skipped ++;
				get();
			}
			
			if(skipped > 0)
			{
				std::cout << "skipped " << skipped << " whitespace chars" << std::endl;
			}
		}
		
		char Parser::peek()
		{
			char result = m_Stream.peek();
			
			std::cout << "peeked '" << (result == '\n' ? "\\n" : std::string(&result, 1)) << "'" << std::endl;
			
			return result;
		}
		
		char Parser::get()
		{
			char result = m_Stream.get();
			
			m_Char ++;
			if(result == '\n')
			{
				m_Char = 1;
				m_Line ++;
			}
			
			std::cout << "[" << m_Line << ":" << m_Char << "] got: '"
				<< (result == '\n' ? "\\n" : std::string(&result, 1)) << "'"
				<< std::endl;
			
			return result;
		}
		
		bool Parser::isEnd() const
		{
			return m_Stream.eof();
		}
		
		void Parser::error(const std::string &_message)
		{
			std::stringstream message;
			
			message << "[line " << m_Line << ", char " << m_Char << "] ";
			message << _message;
			
			throw std::runtime_error(message.str());
		}
		
		void Object::serialise(std::ostream &_stream, int _indent) const
		{
			const std::string Indent = "  ";
			
			auto indent = [&](int _amount) {
				for(int i = 0; i < _amount; i++)
				{
					_stream << Indent;
				}
			};
			
			auto writeValue = [&](){
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
					_stream << '"' << m_Value << '"';
				} break;
			case type::Boolean:
				{
					writeValue();
				} break;
			case type::List:
				{
					_stream << "[" << std::endl;
					
					for(int index = 0; index < m_Elements.size(); index++)
					{
						if(index > 0) _stream << "," << std::endl;
						
						indent(_indent + 1); m_Elements[index].serialise(_stream, _indent + 1);
					}
					
					_stream << std::endl;
					indent(_indent); _stream << "]";
				} break;
			case type::Object:
				{
					_stream << "{" << std::endl;
					
					for(auto iterator = m_Members.begin(); iterator != m_Members.end(); iterator++)
					{
						if(iterator != m_Members.begin()) _stream << "," << std::endl;
						
						indent(_indent + 1); _stream << '"' << iterator->first << '"' << ": ";
						
						iterator->second.serialise(_stream, _indent + 1);
					}
					
					_stream << std::endl;
					indent(_indent); _stream << "}";
				} break;
			default:
				{
					// can't do anything here :x
				} break;
			}
		}
	}
}
