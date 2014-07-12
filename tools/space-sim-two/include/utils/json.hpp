#pragma once
#ifndef _INCLUDE_JSON_HEADER_
#define _INCLUDE_JSON_HEADER_

#include <stdexcept>
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
		
		class Object
		{
		public:
			inline Object() : m_Type(type::Invalid) {}
			inline Object(const std::string &_value) : m_Value(_value), m_Type(type::String) {}
			
			static Object makeObject() { return Object(type::Object); }
			static Object makeList() { return Object(type::List); }
			
			inline std::string asString() const {
				checkType(type::String);
				return m_Value;
			}
			
			inline int asInteger() const {
				checkType(type::Integer);
				return asType<int>();
			}
			
			inline double asDouble() const {
				checkType(type::Decimal);
				return asType<double>();
			}
			
			inline const List asList() const {
				checkType(type::List);
				return m_Elements;
			}
			
			inline const Object &getField(const std::string &_name) {
				checkType(type::Object);
				return m_Members.find(_name)->second;
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
			
		private:
			inline Object(type::Type _type) : m_Type(_type) {}
			
			void checkType(type::Type _type) const { if(m_Type != _type) throw std::runtime_error("json type mismatch"); }
		
		private:
			type::Type m_Type;
			
			std::string m_Value;
			
			List m_Elements;
			Dictionary m_Members;
		};
	}
}

#endif
