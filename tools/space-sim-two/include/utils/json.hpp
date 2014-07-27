#pragma once
#ifndef _INCLUDE_JSON_HEADER_
#define _INCLUDE_JSON_HEADER_

#include <stdexcept>
#include <iostream>
#include <cstdint>
#include <sstream>
#include <vector>
#include <map>

namespace utils
{
	namespace json
	{
		class Object;
		
		typedef std::vector<Object> List;
		typedef std::map<std::string, Object> Dictionary;
		
		namespace type
		{
			enum Type
			{
				Invalid = 0,
				Integer,
				Decimal,
				String,
				Boolean,
				List,
				Object,
				Max
			};
		}
		
		class Parser
		{
		public:
			Parser(std::istream &_stream);
			
			Object parse();
			
		private:
			void parseValue(Object &_value);
			void parseObject(Object &_object);
			void parseString(Object &_string);
			void parseNumeric(Object &_numeric);
			void parseList(Object &_list);
			void parseBool(Object &_boolean);
			
			void expect(const std::string &_expected);
			void skipWhitespace();
			
			char peek();
			char get();
			
			bool isEnd() const;
			
			void error(const std::string &_message);
			
		private:
			std::istream &m_Stream;
			
			unsigned int m_Line;
			unsigned int m_Char;
		};
		
		class Object
		{
		public:
			inline Object() : m_Type(type::Invalid) {}
			inline Object(const std::string &_value) : m_Value(_value), m_Type(type::String) {}
			inline Object(const char *_value) : m_Value(_value), m_Type(type::String) {}
			
			template<typename T>
			inline Object(const T &_value, type::Type _type)
				: m_Type(_type), m_Value(fromType<T>(_value))
			{
			}
			
			inline Object(int _value)
				: m_Type(type::Integer), m_Value(fromType(_value))
			{
			}
			
			inline Object(double _value)
				: m_Type(type::Decimal), m_Value(fromType(_value))
			{
			}
			
			inline Object(bool _value)
				: m_Type(type::Boolean), m_Value(_value ? "true" : "false")
			{
			}
			
			static Object makeObject() { return Object(type::Object); }
			static Object makeList() { return Object(type::List); }
			
			inline type::Type type() const { return m_Type; }
			
			inline bool asBoolean() const {
				checkType(type::Boolean);
				return (m_Value == "true" ? true : false);
			}
			
			inline std::string asString() const {
				return m_Value;
			}
			
			inline int asInteger() const {
				checkTypes({type::Integer, type::Decimal});
				return asType<int>();
			}
			
			inline double asDouble() const {
				checkTypes({type::Decimal, type::Integer});
				return asType<double>();
			}
			
			inline const List asList() const {
				checkType(type::List);
				return m_Elements;
			}
			
			inline void append(const Object &_value) {
				checkType(type::List);
				m_Elements.push_back(_value);
			}
			
			inline const Object &element(unsigned int _index) const {
				checkType(type::List);
				return m_Elements[_index];
			}
			
			inline unsigned int size() const {
				checkType(type::List);
				return m_Elements.size();
			}
			
			inline void remove(unsigned int _index) {
				unsigned int index = 0;
				for(auto iterator = m_Elements.begin();
					iterator != m_Elements.end();
					iterator ++, index++)
				{
					if(index == _index)
					{
						m_Elements.erase(iterator);
						break;
					}
				}
			}
			
			inline const Object &getField(const std::string &_name) {
				checkType(type::Object);
				return m_Members.find(_name)->second;
			}
			
			inline void setField(const std::string &_name, const Object &_value) {
				checkType(type::Object);
				m_Members[_name] = _value;
			}
			
			inline bool hasField(const std::string &_name) const {
				checkType(type::Object);
				return (m_Members.find(_name) != m_Members.end());
			}
			
			inline std::vector<std::string> fields() const {
				checkType(type::Object);
				
				std::vector<std::string> result;
				for(auto iter = m_Members.begin(); iter != m_Members.end(); iter++)
				{
					result.push_back(iter->first);
				}
				
				return result;
			}
			
			template<typename T>
			inline T asType() const {
				std::stringstream convert(m_Value);
				T result;
				convert >> result;
				return result;
			}
			
			inline Object &operator[](const std::string &_name) {
				checkType(type::Object);
				return m_Members[_name];
			}
			
			inline const Object &operator[](const std::string &_name) const {
				checkType(type::Object);
				return m_Members.find(_name)->second;
			}
			
			inline Object &operator[](unsigned int _index) {
				checkType(type::List);
				return m_Elements[_index];
			}
			
			inline const Object &operator[](unsigned int _index) const {
				checkType(type::List);
				return m_Elements.at(_index);
			}
			
			void serialise(std::ostream &_stream, int _indent = 0) const;
			
		private:
			inline Object(type::Type _type) : m_Type(_type) {}
			
			template<typename T>
			std::string fromType(const T &_value)
			{
				std::stringstream convert;
				convert << _value;
				return convert.str();
			}
			
			void checkType(type::Type _type) const { if(m_Type != _type) throw std::runtime_error("json type mismatch"); }
			void checkTypes(const std::vector<type::Type> &_types) const
			{
				for(auto t : _types)
				{
					if(t == m_Type) return;
				}
				
				throw std::runtime_error("json type mismatch");
			}
		
		private:
			type::Type m_Type;
			
			std::string m_Value;
			
			List m_Elements;
			Dictionary m_Members;
		};
		
		inline std::ostream &operator<<(std::ostream &_stream, const Object &_object)
		{
			_object.serialise(_stream);
			return _stream;
		}
		
		inline std::istream &operator>>(std::istream &_stream, Object &_object)
		{
			Parser parser(_stream);
			_object = parser.parse();
			return _stream;
		}
	}
}

#endif
