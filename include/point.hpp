#pragma once

#include <cmath>
#include <iostream>

namespace geo {
    using Real = long double;
    const Real eps = 1e-9;

    struct Point {
        Real x = 0, y = 0;
        
        Point operator+(Point p) const {
            return {x+p.x, y+p.y};
        }

        Point operator-(Point p) const {
            return {x-p.x, y-p.y};
        }

        Point operator*(Real k) const {
            return {x*k, y*k};
        }

        Point operator/(Real k) const {
            return {x/k, y/k};
        }
    };

    using Vector = Point;

    Real dot(Vector a, Vector b) {
        return a.x*b.x + a.y*b.y;
    }

    std::ostream& operator<<(std::ostream& out, Point p) {
        return out << '(' << p.x << ", " << p.y << ")";
    }
}