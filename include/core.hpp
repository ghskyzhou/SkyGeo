/*
Core Lib with Point, Vector, and some simple calculation.
*/

#pragma once

#include <cmath>
#include <iostream>
#include <algorithm>

namespace geo {
    using Real = long double;

    const Real eps = 1e-9;
    const Real pi = acos(-1.0);

    inline int sign(Real x) {
        return (x > eps) - (x < -eps);
    }

    struct Point {
        Real x = 0, y = 0;
    };

    using Vector = Point;

    inline Vector operator+(Vector a, Vector b) {
        return {a.x+b.x, a.y+b.y};
    }

    inline Vector operator-(Vector a, Vector b) {
        return {a.x-b.x, a.y-b.y};
    }

    inline Vector operator*(Vector v, Real k) {
        return {v.x*k, v.y*k};
    }

    inline Vector operator/(Vector v, Real k) {
        return {v.x/k, v.y/k};
    }

    inline bool operator==(Point a, Point b) { // Vector same
        return sign(a.x-b.x) == 0 && sign(a.y-b.y) == 0;
    }

    inline bool operator!=(Point a, Point b) { // Vector same
        return !(a == b);
    }

    inline Real dot(Vector a, Vector b) {
        return a.x*b.x + a.y*b.y;
    }

    inline Real cross(Vector a, Vector b) { // Counter Clockwise
        return a.x*b.y - a.y*b.x;
    }
    
    inline Real cross(Point a, Point b, Point c) {
        return cross(b-a, c-a); // ab x ac
    }

    inline Real norm2(Vector v) {
        return dot(v, v);
    }

    inline Real len(Vector v) {
        return std::sqrt(norm2(v));
    }

    inline Real dis(Point a, Point b) {
        return len(a - b);
    }

    inline Real angle(Vector a, Vector b) { // Cautious with precision issue
        return acos(dot(a, b) / (len(a) * len(b)));
    }

    inline Vector proj(Vector a, Vector b) { // Project b on a
        return a * (dot(a, b) / norm2(a));
    }

    inline Vector rotate(Vector v, Real theta) { // Counter Clockwise
        return {v.x * cos(theta) - v.y * sin(theta), v.x * sin(theta) + v.y * cos(theta)};
    }

    inline int orient(Point a, Point b, Point c) { // a -> b -> c
        return sign(cross(a, b, c));
        // 1 turn left, -1 turn right, 0 line
    }

    inline std::istream& operator>>(std::istream& in, Point& p) {
        return in >> p.x >> p.y;
    }

    inline std::ostream& operator<<(std::ostream& out, const Point& p) {
        return out << '(' << p.x << ", " << p.y << ')';
    }
}