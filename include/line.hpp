/*
Lib with Line and Segment.
*/

#pragma once

#include <cmath>
#include <iostream>
#include <core.hpp>

namespace geo {
    struct Line {
        Point a, b;
    };

    struct Segment {
        Point a, b;

        explicit operator Line() const {
            return {a, b};
        }
        
        explicit operator Vector() const {
            return b-a;
        }
    };

    Point foot(Point p, Line l) {
        return l.a + proj(l.b-l.a, p-l.a);
    }

    Point reflect(Point p, Line l) {
        return foot(p, l)*2 - p;
    }

    int orientLine(Point p, Line l) {
        return orient(l.a, l.b, p); 
    } // 1 left, -1 right, 0 on line
    
    bool checkOnLine(Point p, Line l) {
        return orientLine(p, l) == 0;
    }

    bool checkOnSeg(Point p, Segment s) {
        return checkOnLine(p, (Line)s) && sign(dot(p-s.a, p-s.b)) <= 0;
    }

    Real disPointLine(Point p, Line l) {
        Point ft = foot(p, l);
        return dis(ft, p);
    }

    Real disPointSeg(Point p, Segment s) {
        Point ft = foot(p, (Line)s);
        if(checkOnSeg(ft, s)) {
            return dis(ft, p);
        } else {
            return std::min(dis(p, s.a), dis(p, s.b));
        }
    }

    Vector dir(Line l) { // Only for direction, no length
        return l.b-l.a;
    }

    int relationLine(Line a, Line b) {
        if(sign(cross(dir(a), dir(b))) == 0) {
            return 2;
        } else if(sign(dot(dir(a), dir(b))) == 0) {
            return 1;
        } else {
            return 0;
        }
        // 2 parallel, 1 orthogonal, 0 other
    }

    Point getLineInter(Line a, Line b) {
        Real t = cross(b.a-a.a, dir(b)) / cross(dir(a), dir(b));
        return a.a + dir(a) * t;
    }

    bool checkLineInter(Line a, Line b) {
        return sign(cross(dir(a), dir(b))) != 0;
    }

    bool checkSegInter(Segment a, Segment b) {
        int o1 = orient(a.a, a.b, b.a);
        int o2 = orient(a.a, a.b, b.b);
        int o3 = orient(b.a, b.b, a.a);
        int o4 = orient(b.a, b.b, a.b);

        if (o1 == 0 && checkOnSeg(b.a, a)) return true;
        if (o2 == 0 && checkOnSeg(b.b, a)) return true;
        if (o3 == 0 && checkOnSeg(a.a, b)) return true;
        if (o4 == 0 && checkOnSeg(a.b, b)) return true;

        return o1 * o2 < 0 && o3 * o4 < 0;
    }

    std::istream& operator>>(std::istream& in, Line& l) {
        return in >> l.a >> l.b;
    }

    std::ostream& operator<<(std::ostream& out, const Line& l) {
        return out << "Line [" << l.a << ", " << l.b << ']';
    }

    std::istream& operator>>(std::istream& in, Segment& s) {
        return in >> s.a >> s.b;
    }

    std::ostream& operator<<(std::ostream& out, const Segment& s) {
        return out << "Segment [" << s.a << ", " << s.b << ']';
    }
}