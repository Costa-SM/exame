# circle.py
# Author: João Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from rrt_methods.obstacles.obstacle import Obstacle


class Circle(Obstacle):

    def __init__(self, x: float, y: float, r: float) -> None:
        """
        Class that represents a circle obstacle
        * x: x coordinate of the circle's center
        * y: y coordinate of the circle's center
        * r: radius of the circle
        """
        self.x = x
        self.y = y
        self.r = r

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the circle in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (1 axis)
        """
        ax.autoscale_view()
        ax.add_patch(
            plt.Circle(
                [self.x, self.y],
                self.r,
                facecolor="blue",
                edgecolor="black",
            )
        )

    def distance(self, x: float, y: float) -> float:
        """
        Calculates a point's distance to the circle
        * x: x coordinate of the point
        * y: y coordinate of the point
        """
        return float(np.max((
            np.linalg.norm([self.x - x, self.y - y]) - self.r,
            0
        )))

    @staticmethod
    def __main__():
        fig, ax = plt.subplots()
        ax.set_title("Circle")
        circle = Circle(0, 0, 10)
        circle.plot(fig, ax)
        plt.show()


if __name__ == "__main__":
    Circle.__main__()
