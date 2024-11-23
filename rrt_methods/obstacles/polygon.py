# polygon.py
# Author: João Lucas
# Created: 23.11.2024

import matplotlib.pyplot as plt
import shapely.geometry as geo

from rrt_methods.obstacles.obstacle import Obstacle


class Polygon(Obstacle):

    def __init__(self, xs: list[float], ys: list[float]) -> None:
        """
        Class that represents a polygon obstacle
        * xs: list of x coordinates of the polygon's contour
        * ys: list of y coordinates of the polygon's contour
        """
        self.xys = list(zip(xs, ys))
        self.poly = geo.Polygon(self.xys)

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the polygon in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes
        """
        ax.add_patch(
            plt.Polygon(
                self.xys,
                facecolor="blue",
                edgecolor="black",
            )
        )

    def distance(self, x: float, y: float) -> float:
        """
        Calculates a point's distance to the polygon
        * x: x coordinate of the point
        * y: y coordinate of the point
        """
        return self.poly.distance(geo.Point((x, y)))

    def __main__():
        fig, ax = plt.subplots()
        ax.set_title("Polygon")
        polygon = Polygon([-5, -5, 5, 5], [-5, 5, 5, -5])
        polygon.plot(fig, ax)
        ax.autoscale_view()
        plt.show()


if __name__ == "__main__":
    Polygon.__main__()
