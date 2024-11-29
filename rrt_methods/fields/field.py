# field.py
# Author: Joao Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from rrt_methods.obstacles.obstacle import Obstacle


class Field:
    def __init__(self, shape: tuple[float, float]) -> None:
        """
        Class that represents a field
        * shape: width and height of the field
        """
        self.shape = shape
        self.obstacles = list[Obstacle]()

    def add_obstacle(self, obstacle: Obstacle) -> Field:
        """
        Adds an obstacle to the field
        * obstacle: obstacle to add
        """
        self.obstacles.append(obstacle)
        return self

    def plot(self, ax: Axes) -> None:
        """
        Plots the field in the figure
        * ax: matplotlib Axes object (1 axis)
        """
        ax.set_title("Field Representation")
        ax.set_xlabel("$x$ coordinate (m)")
        ax.set_ylabel("$y$ coordinate (m)")
        ax.plot(
            [0, self.shape[0]],
            [[0, self.shape[1]], [0, self.shape[1]]],
            color="black",
        )
        ax.plot(
            [[0, self.shape[0]], [0, self.shape[0]]],
            [0, self.shape[1]],
            color="black",
        )
        for obstacle in self.obstacles:
            obstacle.plot(ax)

        ax.autoscale_view()

    @staticmethod
    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        _, ax = plt.subplots()
        field = Field((10, 10))
        field.add_obstacle(Circle((3, 3), 2)).add_obstacle(
            Polygon([(6, 6), (6, 8), (8, 8), (8, 6)])
        )
        field.plot(ax)
        ax.autoscale_view()
        plt.show()


if __name__ == "__main__":
    Field.__main__()
