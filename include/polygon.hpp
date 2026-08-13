/*
Lib with Polygon.
*/

#pragma once

#include <core.hpp>
#include <line.hpp>
#include <vector>

namespace geo {
    struct Polygon {
        std::vector <Point> p;

        Polygon() = default;
        
        Polygon(int n) : p(n) {}
        
        Point& operator[](int i) {
            return p[i];
        }

        const Point& operator[](int i) const {
            return p[i];
        }

        int size() const {
            return (int)p.size();
        }

        std::vector <Point> :: iterator begin() {
            return p.begin();
        }

        std::vector <Point> :: iterator end() {
            return p.end();
        }

        std::vector <Point> :: const_iterator begin() const {
            return p.begin();
        }

        std::vector <Point> :: const_iterator end() const {
            return p.end();
        }

        void push_back(Point x) {
            p.push_back(x);
        }

        bool empty() const {
            return p.empty();
        }

        void clear() {
            p.clear();
        }
    };

    inline Real signedArea(const Polygon& p) {
        Real re = 0;
        for(int i = 0; i < p.size(); i++) re += cross(p[i], p[(i+1)%p.size()]);
        return re / 2.0;
        // Shoelace Formula
    }

    inline Real area(const Polygon& p) {
        return std::abs(signedArea(p));
    }
}