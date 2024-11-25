# potential_field.py
# Author: João Lucas
# Created: 24.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from rrt_methods.fields.field import Field


class PotentialField(Field):
    def __init__(
            self,
            width: float,
            height: float,
            margin: float
            ) -> None:
        """
        Class that represents a potential field
        * width: width of the field
        * height: height of the field
        * margin: object's margin size till maximum potential
        """
        super().__init__(width, height)
        self.margin = margin

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the potential field in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (2 axes)
        """
        ax[0].autoscale_view()
        xs, ys = np.meshgrid(
            np.linspace(0, self.width,  100),
            np.linspace(0, self.height, 100)
        )
        ax[0].imshow(
            np.vectorize(self.potential)(xs, ys),
            origin="lower"
        )
        super().plot(fig, ax[1])

    def potential(self, x: float, y: float) -> float:
        """
        Calculates a point's potential
        * x: x coordinate of the point
        * y: y coordinate of the point
        """
        potential = 1.0
        for obstacle in self.obstacles:
            potential *= min(
                1.0,
                obstacle.distance(x, y)/self.margin
            )
        return potential

    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots(ncols=2)
        potential_field = PotentialField(10, 10, 2)
        potential_field.add_obstacle(
            Circle(3, 3, 2)
        ).add_obstacle(
            Polygon([6, 6, 8, 8], [6, 8, 8, 6])
        )
        potential_field.plot(fig, ax)
        plt.show()


if __name__ == "__main__":
    PotentialField.__main__()
