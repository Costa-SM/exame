# rrt.py
# Author: Joao Lucas
# Created: 25.11.2024

from __future__ import annotations

import random

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

from rrt_methods.fields.field import Field
from rrt_methods.trees.tree import Tree


class RRT:
    def __init__(
        self,
        source: tuple[float, float],
        field: Field,
    ) -> None:
        """
        Class that represents a RRT
        * source: source of the path
        * field: field to find a path in
        """
        self.tree = Tree(source)
        self.field = field
        self.max_it = 1000
        self.goal_bias = 0.2
        self.delta = 0.1
        self.eps = 1e-3

    @staticmethod
    def __main__():
        """Performs a test of the RRT class"""
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots()
        rrt = RRT(
            (1, 1),
            Field((10, 10))
            .add_obstacle(Circle((3, 3), 2))
            .add_obstacle(Polygon([(6, 6), (6, 8), (8, 8), (8, 6)])),
        )

        goal_position: tuple[float, float] = (9, 9)
        rrt.plan_path(goal_position)
        rrt.plot(fig, ax, goal_position)
        ax.autoscale_view()
        ax.scatter(goal_position[0], goal_position[1])
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
        self.tree = Tree(self.tree.root.point)

        for _ in range(self.max_it):
            if random.random() < self.goal_bias:
                random_point = goal

            else:
                random_point = self._sample_free_space()

            nearest_node = self.tree.find_nearest(random_point)
            extended_point = nearest_node.extend(random_point, self.delta)

            if not self._check_collision_free(extended_point):
                continue

            nearest_node.add_child(extended_point)

            if np.linalg.norm(np.array(extended_point) - np.array(goal)) < self.eps:
                break

    def plot(self, fig: Figure, ax: Axes, goal_position: tuple[float, float] | None = None) -> None:
        """
        Plots the field and the RRT
        * ax: matplotlib Axes object (1 axis)
        """
        self.field.plot(fig, ax)
        self.tree.plot(fig, ax, goal_position)

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #
    def _check_collision_free(self, point: tuple[float, float]):
        """
        Checks if the selected point collides with one of the obstacles in the field
        * point: (x, y) coordinates of the point
        """
        for obstacle in self.field.obstacles:
            if obstacle.distance(point) == 0:
                return False

        return True

    def _sample_free_space(self) -> tuple[float, float]:
        """
        Randomly samples the field until a point that is not inside an obstacle is found
        """
        while True:
            random_point = (np.random.random(2) * np.array(self.field.shape)).tolist()
            if self._check_collision_free(random_point):
                return random_point


if __name__ == "__main__":
    RRT.__main__()
