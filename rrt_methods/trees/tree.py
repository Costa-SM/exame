# tree.py
# Author: Arthur Stevenson
# Created: 19.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import Axes


class Tree:
    def __init__(self, point: tuple[float, float]) -> None:
        """
        Class that represents a tree data structure
        * point: x and y coordinates of the tree's root node
        """
        self.root = TreeNode(point, None)

    @staticmethod
    def __main__():
        """Performs a test of the Tree class"""
        sample_tree = Tree((0.0, 0.0))
        sample_tree.root.add_child(sample_tree.root.extend((3.0, 3.0), 2.0))
        sample_tree.root.add_child(sample_tree.root.extend((-1.0, 1.0), 2.0))
        sample_tree.root.add_child(sample_tree.root.extend((1.0, -1.0), 2.0))
        sample_tree.root.add_child(sample_tree.root.extend((-1.0, -1.0), 2.0))

        sample_tree.root.children[0].add_child(
            sample_tree.root.children[0].extend((2.0, 2.0), 2.0)
        )

        sample_tree.print()

        _, ax = plt.subplots()
        sample_tree.plot(ax)
        plt.show()

    # -------------------------------------------------------------------------------- #
    # Public Methods
    # -------------------------------------------------------------------------------- #
    def find_nearest(self, point: tuple[float, float]) -> TreeNode:
        """
        Find the nearest tree node to the point
        * point: x and y coordinates of the point
        """
        return self._find_nearest_recursion(self.root, point)

    def print(self):
        """
        Prints a representation of the tree
        """
        self._print_recursion(self.root)

    def plot(self, fig: Figure, ax: Axes, node_position: tuple[float, float] | None = None):
        """
        Creates a plot representing the tree
        * ax: matplotlib Axes object (1 axis)
        * node_position: The position of a node, for printing from it until the root
        """
        self._plot_complete_recursion(self.root, ax)

        if node_position:
            node = self.find_nearest(node_position)
            self._plot_from_child(node, ax)

        ax.autoscale_view()

    # -------------------------------------------------------------------------------- #
    # Private Methods
    # -------------------------------------------------------------------------------- #
    def _find_nearest_recursion(
        self, node: TreeNode, point: tuple[float, float]
    ) -> TreeNode:
        """
        Recursive call to find the nearest tree node to the point
        * node: current recursive call's node
        * point: x and y coordinates of the point
        """
        nearest = node
        nearest_distance: float = float(
            np.linalg.norm(np.array(point) - np.array(nearest.point))
        )

        for child in node.children:
            child_nearest = self._find_nearest_recursion(child, point)
            child_nearest_distance: float = float(
                np.linalg.norm(np.array(point) - np.array(child_nearest.point))
            )

            if child_nearest_distance < nearest_distance:
                nearest = child_nearest
                nearest_distance = child_nearest_distance

        return nearest

    def _print_recursion(self, node: TreeNode, depth: int = 0):
        """
        Recursive call to print the nodes of a tree
        * node: current recursive call's node
        * depth: current recursive call's depth
        """
        print("  " * depth, f"Node ({node.point[0]:.4f}, {node.point[1]:.4f})")

        for child in node.children:
            self._print_recursion(child, depth + 1)

    def _plot_complete_recursion(self, node: TreeNode, ax: Axes):
        """
        Recursive call to plot the nodes of a tree
        * node: current recursive call's node
        * ax: matplotlib Axes object (1 axis)
        """
        # Plot this node
        # plt.plot(node.point[0], node.point[1], "o", color="blue", zorder=1)

        # Plot a line back to the node's parent
        if node.parent:
            ax.plot(
                [node.point[0], node.parent.point[0]],
                [node.point[1], node.parent.point[1]],
                color="tab:orange",
                zorder=1,
            )

        # Continue calling for all children
        for child in node.children:
            self._plot_complete_recursion(child, ax)

    def _plot_from_child(self, node: TreeNode, ax: Axes):
        """
        Recursive call to plot from a given child until the root of the node.
        * node: current recursive call's node
        * ax: matplotlib Axes object (1 axis)
        """
        # Plot a line back to the node's parent
        if node.parent:
            ax.plot(
                [node.point[0], node.parent.point[0]],
                [node.point[1], node.parent.point[1]],
                color="tab:blue",
                zorder=2,
            )

        # Call for parent
        if node.parent:
            self._plot_from_child(node.parent, ax)


class TreeNode:
    def __init__(self, point: tuple[float, float], parent: TreeNode | None) -> None:
        """
        Class that represents a node of a tree used in RRT.
        * point: x and y coordinates of the current node
        * parent: Current node's parent
        """

        self.point: tuple[float, float] = point
        self.parent: TreeNode | None = parent
        self.children: list[TreeNode] = []

    def add_child(self, point: tuple[float, float]):
        """
        Method that creates a new node
        and adds it as a child of the current node
        * point: x and y coordinates of the new node
        """
        new_node: TreeNode = TreeNode(point, self)
        self.children.append(new_node)

    def extend(self, point: tuple[float, float], delta: float) -> tuple[float, float]:
        """
        Method for implementing the RRT that extends
        the current node towards a given point, returning the extension
        * point: x and y coordinates of the given point
        * delta: Maximum distance between the current node and the extension
        """
        distance: float = float(np.linalg.norm(np.array(point) - np.array(self.point)))

        if distance < delta:
            return point

        point_limited = (
            np.array(self.point)
            + delta * (np.array(point) - np.array(self.point)) / distance
        )
        return point_limited  # type: ignore


if __name__ == "__main__":
    Tree.__main__()
