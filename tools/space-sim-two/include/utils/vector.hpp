#pragma once
#ifndef _INCLUDE_VECTOR_HEADER_
#define _INCLUDE_VECTOR_HEADER_

#include <stdexcept>
#include <ostream>
#include <cmath>

namespace utils
{
	template<typename T, unsigned int N=3>
	class Vector
	{
	public:
		inline Vector() { throw std::runtime_error("unimplemented vector dimension"); }
	};
	
	template<typename T>
	class Vector<T, 2>
	{
	public:
		typedef Vector<T, 2> MyType;
		
	public:
		inline Vector() : m_X(T()), m_Y(T()) {}
		inline Vector(T _x, T _y) : m_X(_x), m_Y(_y) {}
		
		inline T x() const { return m_X; }
		inline T y() const { return m_Y; }
		
		inline T magnitude2() const { return (m_X * m_X + m_Y * m_Y); }
		inline T magnitude() const { return sqrt(magnitude2()); }
		
		inline MyType operator+(const MyType &_other) const {
			return Vector<T, 2>(
				m_X + _other.m_X,
				m_Y + _other.m_Y
			);
		}
		
		inline MyType operator-(const MyType &_other) const {
			return Vector<T, 2>(
				m_X - _other.m_X,
				m_Y - _other.m_Y
			);
		}
		
		inline MyType operator*(T _scalar) const {
			return MyType(
				m_X * _scalar,
				m_Y * _scalar
			);
		}
		
		inline MyType operator/(T _scalar) const {
			return MyType(
				m_X / _scalar,
				m_Y / _scalar
			);
		}
		
		inline void operator+=(const MyType &_other) {
			m_X += _other.m_X;
			m_Y += _other.m_Y;
		}
		
		inline void operator-=(const MyType &_other) {
			m_X -= _other.m_X;
			m_Y -= _other.m_Y;
		}
		
		inline void operator*=(T _scalar) {
			m_X *= _scalar;
			m_Y *= _scalar;
		}
		
		inline void operator/=(T _scalar) {
			m_X /= _scalar;
			m_Y /= _scalar;
		}
		
		inline void normalise() {
			*this /= magnitude();
		}
		
		inline MyType normalised() const {
			return *this / magnitude();
		}
		
		void serialise(std::ostream &_stream) const {
			_stream << "(" << m_X << ", " << m_Y << ")";
		}
		
	private:
		T m_X, m_Y;
	};
	
	template<typename T>
	class Vector<T, 3>
	{
	public:
		typedef Vector<T, 3> MyType;
		
	public:
		inline Vector() : m_X(T()), m_Y(T()), m_Z(T()) {}
		inline Vector(T _x, T _y, T _z) : m_X(_x), m_Y(_y), m_Z(_z) {}
		
		inline T x() const { return m_X; }
		inline T y() const { return m_Y; }
		inline T z() const { return m_Z; }
		
		inline T magnitude2() const { return (m_X * m_X + m_Y * m_Y + m_Z * m_Z); }
		inline T magnitude() const { return sqrt(magnitude2()); }
		
		inline MyType operator+(const MyType &_other) const {
			return MyType(
				m_X + _other.m_X,
				m_Y + _other.m_Y,
				m_Z + _other.m_Z
			);
		}
		
		inline MyType operator-(const MyType &_other) const {
			return MyType(
				m_X - _other.m_X,
				m_Y - _other.m_Y,
				m_Z + _other.m_Z
			);
		}
		
		inline MyType operator*(T _scalar) const {
			return MyType(
				m_X * _scalar,
				m_Y * _scalar,
				m_Z * _scalar
			);
		}
		
		inline MyType operator/(T _scalar) const {
			return MyType(
				m_X / _scalar,
				m_Y / _scalar,
				m_Z / _scalar
			);
		}
		
		inline void operator+=(const MyType &_other) {
			m_X += _other.m_X;
			m_Y += _other.m_Y;
			m_Z += _other.m_Z;
		}
		
		inline void operator-=(const MyType &_other) {
			m_X -= _other.m_X;
			m_Y -= _other.m_Y;
			m_Z -= _other.m_Z;
		}
		
		inline void operator*=(T _scalar) {
			m_X *= _scalar;
			m_Y *= _scalar;
			m_Z *= _scalar;
		}
		
		inline void operator/=(T _scalar) {
			m_X /= _scalar;
			m_Y /= _scalar;
			m_Z /= _scalar;
		}
		
		inline void normalise() {
			*this /= magnitude();
		}
		
		inline MyType normalised() const {
			return *this / magnitude();
		}
		
		void serialise(std::ostream &_stream) const {
			_stream << "(" << m_X << ", " << m_Y << ", " << m_Z << ")";
		}
		
	private:
		T m_X, m_Y, m_Z;
	};
	
	template<typename T, unsigned int N>
	std::ostream &operator<<(std::ostream &_stream, const Vector<T, N> &_vector)
	{
		_vector.serialise(_stream);
		return _stream;
	}
};

#endif
