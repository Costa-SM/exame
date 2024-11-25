# field.py
# Author: João Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt

from rrt_methods.obstacles.obstacle import Obstacle


class Field:

    def __init__(self, width: float, height: float) -> None:
        """
        Class that represents a field
        * width: width of the field
        * height: height of the field
        """
        self.width = width
        self.height = height
        self.obstacles = list[Obstacle]()

    def add_obstacle(self, obstacle: Obstacle) -> Field:
        """
        Adds an obstacle to the field
        * obstacle: obstacle to add
        """
        self.obstacles.append(obstacle)
        return self

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the field in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (1 axis)
        """
        ax.autoscale_view()
        ax.set_title("Field")
        ax.set_xlabel("$x$ coordinate (m)")
        ax.set_ylabel("$y$ coordinate (m)")
        ax.plot(
            [0, self.width],
            [[0, self.height], [0, self.height]],
            color="black",
        )
        ax.plot(
            [[0, self.width], [0, self.width]],
            [0, self.height],
            color="black",
        )
        for obstacle in self.obstacles:
            obstacle.plot(fig, ax)

    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots()
        field = Field(10, 10)
        field.add_obstacle(
            Circle(3, 3, 2)
        ).add_obstacle(
            Polygon([6, 6, 8, 8], [6, 8, 8, 6])
        )
        field.plot(fig, ax)
        plt.show()


if __name__ == "__main__":
    Field.__main__()
