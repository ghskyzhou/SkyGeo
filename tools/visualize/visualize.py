from pathlib import Path
import sys
import math

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtWidgets


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

# SkyGeo/tools/visualize/visualize.py
# parents[2] -> SkyGeo/
ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS_DIR = ROOT / "experiments"


# ------------------------------------------------------------
# Parse
# ------------------------------------------------------------

def load_objects(path: Path):
    objects = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            parts = line.split()
            kind = parts[0]

            try:
                if kind == "POINT":
                    if len(parts) != 3:
                        raise ValueError

                    x, y = map(float, parts[1:])
                    objects.append(("POINT", x, y))

                elif kind == "LINE":
                    if len(parts) != 5:
                        raise ValueError

                    x1, y1, x2, y2 = map(float, parts[1:])
                    objects.append(("LINE", x1, y1, x2, y2))

                elif kind == "SEGMENT":
                    if len(parts) != 5:
                        raise ValueError

                    x1, y1, x2, y2 = map(float, parts[1:])
                    objects.append(("SEGMENT", x1, y1, x2, y2))

                else:
                    print(
                        f"Warning: unknown object '{kind}' "
                        f"at line {line_no}"
                    )

            except ValueError:
                print(
                    f"Warning: invalid data at line {line_no}: "
                    f"{line}"
                )

    return objects


# ------------------------------------------------------------
# Bounds
# ------------------------------------------------------------

def get_bounds(objects):
    xs = []
    ys = []

    for obj in objects:
        kind = obj[0]

        if kind == "POINT":
            _, x, y = obj
            xs.append(x)
            ys.append(y)

        elif kind in ("LINE", "SEGMENT"):
            _, x1, y1, x2, y2 = obj

            xs.extend([x1, x2])
            ys.extend([y1, y2])

    if not xs:
        return -5, 5, -5, 5

    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)

    width = xmax - xmin
    height = ymax - ymin

    span = max(width, height, 1.0)
    margin = span * 0.15

    # 避免所有东西都在一条竖线/横线上时视野变成 0
    if width < span * 0.1:
        cx = (xmin + xmax) / 2
        xmin = cx - span * 0.5
        xmax = cx + span * 0.5

    if height < span * 0.1:
        cy = (ymin + ymax) / 2
        ymin = cy - span * 0.5
        ymax = cy + span * 0.5

    return (
        xmin - margin,
        xmax + margin,
        ymin - margin,
        ymax + margin,
    )


# ------------------------------------------------------------
# Draw
# ------------------------------------------------------------

def create_window(objects, experiment_name):
    # 简洁白色主题
    pg.setConfigOptions(
        antialias=True,
        background="w",
        foreground="#374151",
    )

    window = pg.PlotWidget()
    window.resize(900, 800)
    window.setWindowTitle(f"SkyGeo - {experiment_name}")

    plot = window.getPlotItem()
    view = plot.getViewBox()

    # --------------------------------------------------------
    # Native mouse interaction
    #
    # Left drag   -> pan
    # Mouse wheel -> zoom
    # --------------------------------------------------------

    view.setMouseMode(pg.ViewBox.PanMode)
    view.setMouseEnabled(x=True, y=True)

    # 几何坐标的 x/y 比例必须一致
    view.setAspectLocked(True, ratio=1)

    # 不需要右键菜单
    plot.setMenuEnabled(False)

    plot.setTitle(
        f"SkyGeo — {experiment_name}",
        size="13pt",
    )

    plot.setLabel("bottom", "x")
    plot.setLabel("left", "y")

    plot.showGrid(
        x=True,
        y=True,
        alpha=0.18,
    )

    # --------------------------------------------------------
    # Pens
    # --------------------------------------------------------

    point_brush = pg.mkBrush("#E11D48")

    segment_pen = pg.mkPen(
        "#2563EB",
        width=2.2,
    )

    segment_endpoint_brush = pg.mkBrush("#2563EB")

    line_pen = pg.mkPen(
        "#6B7280",
        width=1.5,
        style=QtCore.Qt.PenStyle.DashLine,
    )

    axis_pen = pg.mkPen(
        "#9CA3AF",
        width=1,
    )

    # --------------------------------------------------------
    # Collect primitives
    # --------------------------------------------------------

    point_x = []
    point_y = []

    segment_x = []
    segment_y = []

    segment_endpoint_x = []
    segment_endpoint_y = []

    # --------------------------------------------------------
    # Objects
    # --------------------------------------------------------

    for obj in objects:
        kind = obj[0]

        # ------------------------
        # Point
        # ------------------------

        if kind == "POINT":
            _, x, y = obj

            point_x.append(x)
            point_y.append(y)

        # ------------------------
        # Segment
        # ------------------------

        elif kind == "SEGMENT":
            _, x1, y1, x2, y2 = obj

            # NaN 用来断开不同 segment，
            # 这样所有 segment 可以一次性画出来
            segment_x.extend([x1, x2, math.nan])
            segment_y.extend([y1, y2, math.nan])

            segment_endpoint_x.extend([x1, x2])
            segment_endpoint_y.extend([y1, y2])

        # ------------------------
        # Infinite Line
        # ------------------------

        elif kind == "LINE":
            _, x1, y1, x2, y2 = obj

            dx = x2 - x1
            dy = y2 - y1

            if dx == 0 and dy == 0:
                print(
                    f"Warning: ignored degenerate line "
                    f"({x1}, {y1}) -> ({x2}, {y2})"
                )
                continue

            angle = math.degrees(math.atan2(dy, dx))

            line = pg.InfiniteLine(
                pos=(x1, y1),
                angle=angle,
                pen=line_pen,
                movable=False,
            )

            plot.addItem(line)

    # --------------------------------------------------------
    # Draw points
    # --------------------------------------------------------

    if point_x:
        points = pg.ScatterPlotItem(
            x=point_x,
            y=point_y,
            size=9,
            pen=None,
            brush=point_brush,
            pxMode=True,
        )

        plot.addItem(points)

    # --------------------------------------------------------
    # Draw segments
    # --------------------------------------------------------

    if segment_x:
        segments = pg.PlotDataItem(
            x=segment_x,
            y=segment_y,
            pen=segment_pen,
            connect="finite",
        )

        plot.addItem(segments)

        endpoints = pg.ScatterPlotItem(
            x=segment_endpoint_x,
            y=segment_endpoint_y,
            size=6,
            pen=None,
            brush=segment_endpoint_brush,
            pxMode=True,
        )

        plot.addItem(endpoints)

    # --------------------------------------------------------
    # Coordinate axes
    # --------------------------------------------------------

    x_axis = pg.InfiniteLine(
        pos=0,
        angle=0,
        pen=axis_pen,
        movable=False,
    )

    y_axis = pg.InfiniteLine(
        pos=0,
        angle=90,
        pen=axis_pen,
        movable=False,
    )

    plot.addItem(x_axis)
    plot.addItem(y_axis)

    # --------------------------------------------------------
    # Initial view
    # --------------------------------------------------------

    xmin, xmax, ymin, ymax = get_bounds(objects)

    view.setRange(
        xRange=(xmin, xmax),
        yRange=(ymin, ymax),
        padding=0,
    )

    return window


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  visualize <experiment>")
        sys.exit(1)

    experiment = sys.argv[1]

    experiment_dir = EXPERIMENTS_DIR / experiment
    vis_file = experiment_dir / "visualize.out"

    if not experiment_dir.exists():
        print(
            f"Error: experiment not found: "
            f"{experiment}"
        )
        sys.exit(1)

    if not vis_file.exists():
        print("Error: visualize.out not found:")
        print(f"  {vis_file}")
        print()
        print("Run the experiment with draw(...) first.")
        sys.exit(1)

    objects = load_objects(vis_file)

    if not objects:
        print(
            "Error: visualize.out contains "
            "no drawable objects."
        )
        sys.exit(1)

    print(f"Experiment : {experiment}")
    print(f"Input      : {vis_file.relative_to(ROOT)}")
    print(f"Objects    : {len(objects)}")

    app = (
        QtWidgets.QApplication.instance()
        or QtWidgets.QApplication(sys.argv)
    )

    window = create_window(
        objects,
        experiment,
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()