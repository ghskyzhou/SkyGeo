/*
Core Lib with Point, Vector, and some simple calculation.
*/

#pragma once

#include <cmath>
#include <iostream>

namespace geo {
    // Definition
    using Real = long double;
    const Real eps = 1e-9;
    const Real pi = acos(-1.0);

    int sign(Real x) {
        return (x > eps) - (x < -eps);
    }

    struct Point {
        Real x = 0, y = 0;
    };

    using Vector = Point;

    // Simple Operator
    Vector operator+(Vector a, Vector b) {
        return {a.x+b.x, a.y+b.y};
    }

    Vector operator-(Vector a, Vector b) {
        return {a.x-b.x, a.y-b.y};
    }

    Vector operator*(Vector v, Real k) {
        return {v.x*k, v.y*k};
    }

    Vector operator/(Vector v, Real k) {
        return {v.x/k, v.y/k};
    }

    bool operator==(Point a, Point b) { // Vector same
        return sign(a.x-b.x) == 0 && sign(a.y-b.y) == 0;
    }

    bool operator!=(Point a, Point b) { // Vector same
        return !(a == b);
    }

    // Complex Operator
    Real dot(Vector a, Vector b) {
        return a.x*b.x + a.y*b.y;
    }

    Real cross(Vector a, Vector b) { // Counter Clockwise
        return a.x*b.y - a.y*b.x;
    }
    
    Real cross(Point a, Point b, Point c) {
        return cross(b-a, c-a); // ab x ac
    }

    Real norm2(Vector v) {
        return dot(v, v);
    }

    Real len(Vector v) {
        return std::sqrt(norm2(v));
    }

    Real dis(Point a, Point b) {
        return len(a - b);
    }

    Real angle(Vector a, Vector b) { // Cautious with precision issue
        return acos(dot(a, b) / (len(a) * len(b)));
    }

    Vector proj(Vector a, Vector b) { // Project b on a
        return a * (dot(a, b) / norm2(a));
    }

    Vector rotate(Vector v, Real theta) { // Counter Clockwise
        return {v.x * cos(theta) - v.y * sin(theta), v.x * sin(theta) + v.y * cos(theta)};
    }

    // Judgement
    int orient(Point a, Point b, Point c) { // a -> b -> c
        return sign(cross(a, b, c));
        // 1 turn left, -1 turn right, 0 line
    }

    // IO Stream
    std::istream& operator>>(std::istream& in, Point& p) {
        return in >> p.x >> p.y;
    }

    std::ostream& operator<<(std::ostream& out, const Point& p) {
        return out << '(' << p.x << ", " << p.y << ')';
    }
}