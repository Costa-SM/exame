# tree.py
# Author: Arthur Stevenson
# Created: 19.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


class Tree:
    def __init__(self, point: tuple[float, float]) -> None:
        """
        Class that represents a tree data structure
        * point: x and y coordinates of the tree's root node
        """
        self.root = TreeNode(point, None)

    def print(self):
        """
        Prints a representation of the tree
        """
        self._print_recursion(self.root)

    def _print_recursion(self, node: TreeNode, depth: int = 0):
        """
        Recursive call to print the nodes of a tree
        * node: current recursive call's node
        * depth: current recursive call's depth
        """
        print(
            "  " * depth,
            f"Node ({node.point[0]:.4f}, {node.point[1]:.4f})"
        )

        for child in node.children:
            self._print_recursion(child, depth + 1)

    def plot(self, fig: plt.Figure, ax: plt.Axes):
        """
        Creates a plot representing the tree
        * fig: pyplot's figure
        * ax: pyplot's axes (1 axis)
        """
        plt.title("Tree Representation")
        plt.xlabel("$x$ coordinate (m)")
        plt.ylabel("$y$ coordinate (m)")
        self._plot_recursion(self.root, fig, ax)

        plt.show()

    def _plot_recursion(self, node: TreeNode, fig: plt.Figure, ax: plt.Axes):
        """
        Recursive call to plot the nodes of a tree
        * node: current recursive call's node
        * fig: pyplot's figure
        * ax: pyplot's axes (1 axis)
        """
        # Plot this node
        plt.plot(node.point[0], node.point[1], "o", color="blue", zorder=1)

        # Plot a line back to the node's parent
        if node.parent:
            plt.plot(
                [node.point[0], node.parent.point[0]],
                [node.point[1], node.parent.point[1]],
                color="orange",
                zorder=0,
            )

        # Continue calling for all children
        for child in node.children:
            self._plot_recursion(child, fig, ax)

    @staticmethod
    def __main__():
        sample_tree = Tree((0.0, 0.0))
        sample_tree.root.extend((3.0, 3.0), 2.0)
        sample_tree.root.extend((-1.0, 1.0), 2.0)
        sample_tree.root.extend((1.0, -1.0), 2.0)
        sample_tree.root.extend((-1.0, -1.0), 2.0)

        sample_tree.root.children[0].extend((2.0, 2.0), 2.0)

        sample_tree.print()

        fig, ax = plt.subplots()
        sample_tree.plot(fig, ax)
        ax.autoscale_view()
        plt.show()


class TreeNode:
    def __init__(
            self,
            point: tuple[float, float],
            parent: TreeNode | None
            ) -> None:
        """
        Class that represents a node of a tree used in RRT.
        * point: x and y coordinates of the current node
        * parent: Current node's parent
        """

        self.point: tuple[float, float] = point
        self.parent: TreeNode | None = parent
        self.children: list[TreeNode] = []

    def _add_child(self, point: tuple[float, float]):
        """
        Method that creates a new node
        and adds it as a child of the current node
        * point: x and y coordinates of the new node
        """
        new_node: TreeNode = TreeNode(point, self)
        self.children.append(new_node)

    def extend(self, point: tuple[float, float], delta: float):
        """
        Method for implementing the RRT that extends
        the current node towards a given point
        * point: x and y coordinates of the given point
        * delta: Maximum distance between the current node and the extension
        """
        distance: float = float(np.linalg.norm(
            np.array(point) - np.array(self.point)
        ))

        if distance < delta:
            self._add_child(point)
        else:
            point_limited = np.array(self.point) + \
                delta * (np.array(point) - np.array(self.point)) / distance
            self._add_child(point_limited)


if __name__ == "__main__":
    Tree.__main__()
