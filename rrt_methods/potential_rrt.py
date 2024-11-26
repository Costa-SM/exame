# rrt.py
# Author: João Lucas
# Created: 25.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import random

from rrt_methods.potential_fields.potential_field import PotentialField
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
        self.tree = Tree(source)
        self.potential_field = potential_field
        self.max_it = 1000
        self.goal_bias = 0.2
        self.delta = 0.1
        self.eps = 1e-3

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the potential_field in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (2 axes)
        """
        self.potential_field.plot(fig, ax)
        self.tree.plot(fig, ax[1])

    def _check_collision_free(self, point: tuple[float, float]):
        ok = True
        for obstacle in self.potential_field.obstacles:
            if obstacle.distance(point) == 0:
                ok = False
        return ok

    def _sample_free_space(self) -> tuple[float, float]:
        while True:
            random_point = (
                np.random.random(2)*np.array(self.potential_field.shape)
            ).tolist()
            if self._check_collision_free(random_point):
                return random_point

    def plan_path(
            self,
            goal: tuple[float, float]
            ) -> None:
        self.tree = Tree(self.tree.root.point)
        for it in range(self.max_it):
            if random.random() < self.goal_bias:
                random_point = goal
            else:
                random_point = self._sample_free_space()
            nearest_node = self.tree.find_nearest(
                random_point
            )
            extended_point = nearest_node.extend(
                random_point, self.delta
            )
            if not self._check_collision_free(extended_point):
                continue
            if not random.random() < self.potential_field.potential(
                extended_point
            ):
                continue
            nearest_node.add_child(extended_point)
            if np.linalg.norm(
                np.array(extended_point) - np.array(goal)
            ) < self.eps:
                break

    @staticmethod
    def __main__():
        from rrt_methods.obstacles.circle import Circle
        from rrt_methods.obstacles.polygon import Polygon

        fig, ax = plt.subplots(ncols=2)
        rrt = PotentialRRT(
            (1, 1),
            PotentialField((10, 10), 2).add_obstacle(
                Circle((3, 3), 2)
            ).add_obstacle(
                Polygon([(6, 6), (6, 8), (8, 8), (8, 6)])
            )
        )
        rrt.plan_path((9, 9))
        rrt.plot(fig, ax)
        ax.autoscale_view()
        plt.show()


if __name__ == "__main__":
    PotentialRRT.__main__()
