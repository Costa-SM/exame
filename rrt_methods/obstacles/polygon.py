# polygon.py
# Author: Joao Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import shapely.geometry as geo
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from rrt_methods.obstacles.obstacle import Obstacle


class Polygon(Obstacle):
    def __init__(self, points: list[tuple[float, float]]) -> None:
        """
        Class that represents a polygon obstacle
        * points: list of x and y coordinates of the polygon's contour
        """
        self.points = points
        self.poly = geo.Polygon(points)

    @staticmethod
    def __main__():
        fig, ax = plt.subplots()
        ax.set_title("Polygon")
        polygon = Polygon([(6, 6), (6, 8), (8, 8), (8, 6)])
        polygon.plot(fig, ax)
        ax.autoscale()
        plt.show()

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #

    def plot(self, fig: Figure, ax: Axes) -> None:
        """
        Plots the polygon in the figure
        * ax: pyplot's axes (1 axis)
        """
        ax.add_patch(
            plt.Polygon(  # type: ignore
                self.points,
                facecolor="blue",
                edgecolor="black",
            )
        )

    def distance(self, point: tuple[float, float]) -> float:
        """
        Calculates a point's distance to the polygon
        * x: x coordinate of the point
        * y: y coordinate of the point
        """
        return self.poly.distance(geo.Point(point))


if __name__ == "__main__":
    Polygon.__main__()
