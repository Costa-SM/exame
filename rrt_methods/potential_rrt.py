# rrt.py
# Author: Joao Lucas
# Created: 25.11.2024

from __future__ import annotations

from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from rrt_methods.fields.field import Field
from rrt_methods.potential_fields.potential_field import PotentialField
from rrt_methods.probability_fields.probability_field import ProbabilityField
from rrt_methods.trees.tree import Tree


class PotentialRRT:
    def __init__(
        self,
        source: tuple[float, float],
        potential_field: PotentialField,
    ) -> None:
        """
        Class that represents a potential RRT
        * source: source of the path
        * potential_field: potential field to find a path in
        """
        self.tree: Tree = Tree(source)
        self.potential_field: PotentialField = potential_field
        self.max_it: int = 1500
        self.goal_bias: float = 0.2
        self.delta: float = 0.1
        self.epsilon: float = 1e-1
        self.probability_field: ProbabilityField | None = None

    @staticmethod
    def __main__():
        """Performs a test of the PotentialRRT class"""
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        print("Starting Potential RRT test...")

        fig, ax = plt.subplots(ncols=2)
        rrt = PotentialRRT(
            (1, 1),
            PotentialField((10, 10), 1.5)
            .add_obstacle(Circle((3, 3), 2))
            .add_obstacle(Polygon([(6, 6), (6, 8), (8, 8), (8, 6)]))
            .add_attractor((9, 9), 2),
        )

        start = datetime.now()
        rrt.probability_field = ProbabilityField(rrt.potential_field)
        print(f"2D PDF Generated in {(datetime.now() - start).total_seconds()}s")

        goal: tuple[float, float] = (9, 9)
        rrt.plan_path(goal)
        rrt.plot(fig, ax, goal)
        plt.show()

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #
    def plan_path(self, goal: tuple[float, float]) -> None:
        """
        Attempts to plan a path from the origin (0.0, 0.0) to the goal position using
        the Potential RRT method
        * goal: (x, y) coordinates of the point
        """
        planning_start: datetime = datetime.now()

        self.tree = Tree(self.tree.root.point)

        for _ in range(self.max_it):
            # Sample the field until a point that is not inside an obstacle is found
            while True:
                random_point = self._sample_free_space()
                nearest_node = self.tree.find_nearest(random_point)
                extended_point = nearest_node.extend(random_point, self.delta)

                if self._check_collision_free(extended_point):
                    break

            nearest_node.add_child(extended_point)

            if np.linalg.norm(np.array(extended_point) - np.array(goal)) < self.epsilon:
                print(
                    "Solution found in "
                    f"{(datetime.now() - planning_start).total_seconds()} seconds"
                )
                return

        print("Maximum search iterations reached!")

    def plot(self, fig: Figure, ax: Axes, goal_position: tuple[float, float] | None = None) -> None:
        """
        Plots fields and the Potential RRT
        * fig: matplotlib Figure object
        * ax: matplotlib Axes object (2 axis)
        """
        # Plot the field and the 2D PDF
        Field.plot(self.potential_field, fig, ax[0])  # type: ignore
        self.tree.plot(fig, ax[0], node_position=goal_position)  # type: ignore

        if self.probability_field:
            self.probability_field.plot(fig, ax[1])  # type: ignore
            self.tree.plot(fig, ax[1], node_position=goal_position)  # type: ignore

        ax[0].autoscale_view()  # type: ignore
        ax[1].autoscale_view()  # type: ignore

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #
    def _check_collision_free(self, point: tuple[float, float]):
        """
        Checks if the selected point collides with one of the obstacles in the field
        * point: (x, y) coordinates of the point
        """
        for obstacle in self.potential_field.obstacles:
            if obstacle.distance(point) == 0:
                return False

        return True

    def _sample_free_space(self) -> tuple[float, float]:
        """Samples the probability field for a random point in the field"""
        if self.probability_field:
            return self.probability_field.rvs(num_points=1)[0]

        else:
            raise Exception("Probability field undefined!")


if __name__ == "__main__":
    PotentialRRT.__main__()
