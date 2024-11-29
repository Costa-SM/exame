# probability_field.py
# Authors: Arthur Stevenson, Joao Lucas
# Created: 28.11.2024

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from scipy.integrate import dblquad

from rrt_methods.potential_fields.potential_field import PotentialField


class ProbabilityField:
    def __init__(self, field: PotentialField):
        """
        Class that creates a 2D Probability Density Function for a given Potential Field
        and allows sampling it for points
        * field: The PotentialField that will be used for generating the PDF
        """
        # Store the field as well as its maximum and minimum potential values
        self.field: PotentialField = field
        self.pot_min, self.pot_max = self.field.compute_potential_range(
            linspace_len=100
        )

        # Compute the normalization factor for the PDF
        self.normalization_factor, _ = dblquad(  # type: ignore
            lambda x, y: self.pot_max - self.field.potential((x, y)),
            0.0,
            self.field.shape[0],
            0.0,
            self.field.shape[1],
            epsrel=1e-2,
        )

    @staticmethod
    def __main__():
        """Performs a test of the ProbabilityField class"""
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        # Configure the potential field
        potential_field = (
            PotentialField((10, 10), 1.5)
            .add_obstacle(Circle((3, 3), 2))
            .add_obstacle(Polygon([(6, 6), (6, 8), (8, 8), (8, 6)]))
            .add_attractor((9, 9), 0.5)
        )

        # Probability field
        probability_field = ProbabilityField(potential_field)

        # Create the plot
        fig, ax = plt.subplots(ncols=2, nrows=2)
        probability_field.field.plot_field(ax[0, 0])
        probability_field.field.plot(fig, ax[0, 1])

        # Sample points from the distribution
        points = probability_field.rvs(num_points=4000)
        ax[1, 0].scatter(points[:, 0], points[:, 1], s=5, c="red")  # type: ignore
        ax[1, 0].set_title("Sampled Points")
        ax[1, 0].set_xlabel("$x$ coordinate (m)")
        ax[1, 0].set_ylabel("$y$ coordinate (m)")

        # Plot the probability field
        probability_field.plot(fig, ax[1, 1])

        plt.show()

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #
    def rvs(self, num_points=1, seed=None) -> list[tuple[float, float]]:
        """
        Returns a sample drawn from the 2D Probability Density Function
        * num_points: Number of points that will be sampled from the field
        * seed: Seed of the random number generator
        """
        rng = np.random.default_rng(seed)

        samples = []
        for _ in range(num_points):
            while True:
                # Sample uniformly in the bounding box
                x = rng.uniform(0, self.field.shape[0])
                y = rng.uniform(0, self.field.shape[1])

                # Accept/reject based on PDF value
                if rng.uniform(0, 1) < self._pdf(x, y):
                    samples.append((x, y))
                    break

        return np.array(samples)  # type: ignore

    def plot(self, fig: Figure, ax: Axes) -> None:
        """
        Plots the 2D Probability Density Function
        fig: matplotlib Figure object
        ax: matplotlib Axes object (1 axis)
        """
        points = np.meshgrid(
            np.linspace(0, self.field.shape[0], 100),
            np.linspace(0, self.field.shape[1], 100),
        )
        probabilities = np.vectorize(lambda x, y: self._pdf(x, y))(*points)

        x, y = points
        contour = ax.contourf(x, y, probabilities, levels=50, cmap="inferno", zorder=0)

        # Create the plot
        fig.colorbar(contour, label="Probability", ax=ax)
        ax.set_title("2D Probability Density Function")
        ax.set_xlabel("$x$ coordinate (m)")
        ax.set_ylabel("$y$ coordinate (m)")
        ax.autoscale_view()

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #
    def _pdf(self, x: float, y: float) -> float:
        """
        Calculate the probability of choosing the point defined by the given coordinates
        * x: Point's x coordinate
        * y: Point's y coordinate
        """

        # PDF is defined only inside the PotentialField area
        if (
            (x < 0.0)
            or (x > self.field.shape[0])
            or (y < 0.0)
            or (y > self.field.shape[1])
        ):
            return 0.0

        return (self.pot_max - self.field.potential((x, y))) / self.normalization_factor


if __name__ == "__main__":
    ProbabilityField.__main__()
