# potential_field.py
# Author: João Lucas
# Created: 24.11.2024

from __future__ import annotations

import math
import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as spi

from rrt_methods.fields.field import Field
from rrt_methods.obstacles.obstacle import Obstacle


class PotentialField(Field):
    def __init__(
            self,
            shape: tuple[float, float],
            margin: float
            ) -> None:
        """
        Class that represents a potential field
        * shape: width and height of the field
        * margin: object's margin size till maximum potential
        """
        super().__init__(shape)
        self.margin = margin
        self.normal_factor = math.prod(shape)

    def add_obstacle(self, obstacle: Obstacle) -> PotentialField:
        """
        Adds an obstacle to the potential field
        * obstacle: obstacle to add
        """
        super().add_obstacle(obstacle)
        self.normal_factor = self.normal_factor * spi.dblquad(
            lambda x, y: self.potential((x, y)),
            0, self.shape[0],
            0, self.shape[1],
            epsrel=1e-2
        )[0]
        return self

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the potential field in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (2 axes)
        """
        points = np.meshgrid(
            np.linspace(0, self.shape[0], 100),
            np.linspace(0, self.shape[1], 100)
        )
        ax[0].imshow(
            np.vectorize(lambda x, y: self.potential((x, y)))(*points),
            origin="lower"
        )
        super().plot(fig, ax[1])

    def potential(self, point: tuple[float, float]) -> float:
        """
        Calculates a point's potential
        * x: x coordinate of the point
        * y: y coordinate of the point
        """
        potential = 1.0
        for obstacle in self.obstacles:
            possible_potential = obstacle.distance(point)/self.margin
            if possible_potential < potential:
                potential = possible_potential
        return potential/self.normal_factor

    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots(ncols=2)
        potential_field = PotentialField((10, 10), 2)
        potential_field.add_obstacle(
            Circle((3, 3), 2)
        ).add_obstacle(
            Polygon([(6, 6), (6, 8), (8, 8), (8, 6)])
        )
        potential_field.plot(fig, ax)
        ax[0].autoscale_view()
        ax[1].autoscale_view()
        plt.show()


if __name__ == "__main__":
    PotentialField.__main__()
