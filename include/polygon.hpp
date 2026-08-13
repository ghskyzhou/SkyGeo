/*
Lib with Polygon.
*/

#pragma once

#include <core.hpp>
#include <line.hpp>
#include <vector>

namespace geo {
    struct Polygon {
        // Strictly Counter Clockwise
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
        int n = p.size();
        Real re = 0;
        for(int i = 0; i < n; i++) re += cross(p[i], p[(i+1)%n]);
        return re / 2.0;
        // Shoelace Formula
    }

    inline Real area(const Polygon& p) {
        return std::abs(signedArea(p));
    }

    inline void makeCCW(Polygon& p) {
        // Switch Clockwise polygon to Counter Clockwise
        if(sign(signedArea(p)) < 0) {
            std::reverse(p.begin(), p.end());
        }
    }

    inline bool isConvex(const Polygon& p) {
        int n = p.size();
        for(int i = 0; i < n-1; i++) {
            if(orient(p[i], p[i+1], p[(i+2)%n]) == -1) return false;
        }
        return true;
    }

    inline std::istream& operator>>(std::istream& in, Polygon& poly) {
        int n;
        in >> n;
        poly.p.resize(n);
        for(int i = 0; i < n; i++) {
            in >> poly[i];
        }
        return in;
    }

    inline std::ostream& operator<<(std::ostream& out, const Polygon& poly) {
        out << poly.size() << '\n';
        for(Point p : poly) {
            out << p << '\n';
        }
        return out;
    }
}