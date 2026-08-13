/*
Visualize Lib for working with Python.
*/

#pragma once

#include <fstream>
#include <iomanip>
#include <limits>

#include <core.hpp>
#include <line.hpp>
#include <polygon.hpp>
#include <circle.hpp>

#ifndef SKYGEO_VIS_FILE
#define SKYGEO_VIS_FILE "visualize.out"
#endif

namespace geo {

    inline std::ofstream& visualOut() {
        static std::ofstream out(
            SKYGEO_VIS_FILE,
            std::ios::out | std::ios::trunc
        );
        return out;
    }

    inline void draw(Point p) {
        visualOut()
            << std::setprecision(std::numeric_limits<Real>::max_digits10)
            << "POINT "
            << p.x << ' ' << p.y << '\n';
    }

    inline void draw(Line l) {
        visualOut()
            << std::setprecision(std::numeric_limits<Real>::max_digits10)
            << "LINE "
            << l.a.x << ' ' << l.a.y << ' '
            << l.b.x << ' ' << l.b.y << '\n';
    }

    inline void draw(Segment s) {
        visualOut()
            << std::setprecision(std::numeric_limits<Real>::max_digits10)
            << "SEGMENT "
            << s.a.x << ' ' << s.a.y << ' '
            << s.b.x << ' ' << s.b.y << '\n';
    }

    inline void draw(const Polygon& polygon) {
        std::ofstream& out = visualOut();

        out
            << std::setprecision(std::numeric_limits<Real>::max_digits10)
            << "POLYGON " << polygon.size();

        for(const Point& point : polygon) {
            out << ' ' << point.x << ' ' << point.y;
        }

        out << '\n';
    }

}
