# circle.py
# Author: Joao Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from rrt_methods.obstacles.obstacle import Obstacle


class Circle(Obstacle):

    def __init__(self, center: tuple[float, float], r: float) -> None:
        """
        Class that represents a circle obstacle
        * center: x and y coordinates of the circle's center
        * r: radius of the circle
        """
        self.center = center
        self.r = r

    def plot(self, ax: Axes) -> None:
        """
        Plots the circle in the figure
        * ax: pyplot's axes (1 axis)
        """
        ax.add_patch(
            plt.Circle(  # type: ignore
                self.center,
                self.r,
                facecolor="blue",
                edgecolor="black",
            )
        )

        ax.autoscale_view()

    def distance(self, point: tuple[float, float]) -> float:
        """
        Calculates a point's distance to the circle
        * point: x and y coordinates of the point
        """
        return float(
            np.max(
                [np.linalg.norm(np.array(point) - np.array(self.center)) - self.r, 0.0]
            )
        )

    @staticmethod
    def __main__():
        _, ax = plt.subplots()
        ax.set_title("Circle")
        circle = Circle((3, 3), 2)
        circle.plot(ax)
        plt.show()


if __name__ == "__main__":
    Circle.__main__()
