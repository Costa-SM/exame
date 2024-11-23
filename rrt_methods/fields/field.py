# field.py
# Author: João Lucas
# Created: 23.11.2024

from __future__ import annotations

from rrt_methods.obstacles.obstacle import Obstacle

import matplotlib.pyplot as plt


class Field:

    def __init__(self, width: float, height: float) -> None:
        """
        Class that represents a field
        * width: width of the field
        * height: height of the field
        * obstacles: list of obstacles in the field
        """
        self.width = width
        self.height = height
        self.obstacles = list[Obstacle]()

    def add_obstacle(self, obstacle: Obstacle) -> Field:
        """Adds an obstacle to the field"""
        self.obstacles.append(obstacle)
        return self

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """Plots the field in the figure"""
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
        fig, ax = plt.subplots()
        field = Field(10, 10)
        field.plot(fig, ax)
        ax.autoscale_view()
        plt.show()


if __name__ == "__main__":
    Field.__main__()
