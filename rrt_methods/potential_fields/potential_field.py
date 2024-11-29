# potential_field.py
# Author: Joao Lucas
# Created: 24.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from rrt_methods.fields.field import Field
from rrt_methods.obstacles.obstacle import Obstacle


class PotentialField(Field):
    def __init__(self, shape: tuple[float, float], margin: float) -> None:
        """
        Class that represents a potential field
        * shape: width and height of the field
        * margin: object's margin size until the maximum potential
        """
        super().__init__(shape)
        self.margin = margin

        # Attractors are an (x, y, q) tuple, representing position in space and charge
        self.attractors: list[tuple[float, float, float]] = []
        self.epsilon: float = 1e-3
        self.v_max: float = 10.0

    @staticmethod
    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots(ncols=2)

        # Configure the potential field
        potential_field = (
            PotentialField((10, 10), 2)
            .add_obstacle(Circle((3, 3), 2))
            .add_obstacle(Polygon([(6, 6), (6, 8), (8, 8), (8, 6)]))
            .add_attractor((9, 9), 2)
        )

        # Get information about the potential field
        min_potential, max_potential = potential_field.compute_potential_range(
            linspace_len=100
        )
        print(
            "Minimum and maximum potential values: "
            f"({min_potential:.3f}, {max_potential:.3f})"
        )

        # Plot the potential field and the general field
        potential_field.plot_field(ax[0])
        potential_field.plot(fig, ax[1])
        plt.show()

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #
    def add_obstacle(self, obstacle: Obstacle) -> PotentialField:
        """
        Adds an obstacle to the Potential Field. Obstacles are considered as positively
        charged objects for the purposes of calculating the potential
        * obstacle: Obstacle to be added, should be an `Obstacle` object
        """
        super().add_obstacle(obstacle)

        return self

    def add_attractor(self, point: tuple[float, float], charge) -> PotentialField:
        """
        Adds an attractor to the Potential Field. Attractors are negatively charged
        points in space
        * point: (x, y) coordinates of the attractor
        * charge: The attractor's charge for calculating the potential
        """
        self.attractors.append((point[0], point[1], charge))

        return self

    def plot_field(self, fig: Figure, ax: Axes) -> None:
        """
        Plots the Modeled Field
        * fig: matplotlib Figure object
        * ax: matplotlib Axes object (1 axes)
        """
        super().plot(ax)  # type: ignore

    def plot(self, fig: Figure, ax: Axes) -> None:
        """
        Plots the Potential Field
        * fig: matplotlib Figure object
        * ax: matplotlib Axes object (1 axes)
        """

        points = np.meshgrid(
            np.linspace(0, self.shape[0], 100), np.linspace(0, self.shape[1], 100)
        )
        potentials = np.vectorize(lambda x, y: self.potential((x, y)))(*points)

        x, y = points
        c = ax.contourf(x, y, potentials, levels=50, cmap="viridis")  # type: ignore
        fig.colorbar(c, location="right", label="Potential")

        ax.set_title("Potential Field")  # type: ignore
        ax.set_xlabel("$x$ coordinate (m)")  # type: ignore
        ax.set_ylabel("$y$ coordinate (m)")  # type: ignore
        ax.autoscale_view()

    def compute_potential_range(self, linspace_len: int) -> tuple[float, float]:
        """
        Computes the highest and lowest potential values in the Potential Field.
        * return: (minimum_potential, maximum_potential)
        * linspace_len: Number of points used to discretize the field when calculating
        the potential values
        """
        points = np.meshgrid(
            np.linspace(0, self.shape[0], linspace_len),
            np.linspace(0, self.shape[1], linspace_len),
        )
        potentials = np.vectorize(lambda x, y: self.potential((x, y)))(*points)

        return (np.min(potentials), np.max(potentials))

    def potential(self, point: tuple[float, float]) -> float:
        """
        Calculates an estimate of the given point's potential. In the potential field,
        obstacles are positive charges, and attractors are negative ones.
        * point: (x, y) coordinates of the point
        """
        potential: float = 0.0

        for attractor in self.attractors:
            distance = np.linalg.norm(
                np.array([attractor[0], attractor[1]]) - np.array(point)
            )

            if distance < self.epsilon:
                distance = self.epsilon

            potential -= attractor[2] / distance  # type: ignore

        for obstacle in self.obstacles:
            distance = obstacle.distance(point)

            if distance < self.epsilon:
                return self.v_max

            multiplier = np.max([1 - distance / self.margin, 0.0])

            potential += self.v_max * multiplier

        return potential


if __name__ == "__main__":
    PotentialField.__main__()
