# tree.py
# Author: Arthur Stevenson
# Created: 19.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np


class Tree:

    max_nodes: int
    root: TreeNode

    def __init__(self, x: float, y: float) -> None:
        """
        Class that represents a tree data structure
        * x: x coordinate of the tree's root node
        * y: y coordinate of the tree's root node
        """
        self.root = TreeNode(x, y, None)

    def print(self):
        """
        Prints a representation of the tree
        """
        self._print_tree_recursion(self.root)

    def _print_recursion(self, node: TreeNode, depth: int = 0):
        """
        Recursive call to print the nodes of a tree
        """
        print("  " * depth, f"Node ({node.x:.4f}, {node.y:.4f})")

        for child in node.children:
            self._print_recursion(child, depth + 1)

    def plot(self):
        """
        Creates a plot representing the tree
        """
        plt.title("Tree Representation")
        plt.xlabel("$x$ coordinate (m)")
        plt.ylabel("$y$ coordinate (m)")
        self._plot_recursion(self.root)

        plt.show()

    def _plot_recursion(self, node: TreeNode):
        """
        Recursive call to plot the nodes of a tree
        """
        # Plot this node
        plt.plot(node.x, node.y, "o", color="tab:blue", zorder=1)

        # Plot a line back to the node's parent
        if node.parent:
            plt.plot(
                [node.x, node.parent.x],
                [node.y, node.parent.y],
                color="tab:orange",
                zorder=0,
            )

        # Continue calling for all children
        for child in node.children:
            self._plot_recursion(child)


class TreeNode:
    def __init__(self, x: float, y: float, parent: TreeNode | None) -> None:
        """
        Class that represents a node of a tree used in RRT.
        * x: x coordinate of the current node
        * y: y coordinate of the current node
        * parent: Current node's parent
        """

        self.x: float = x
        self.y: float = y
        self.parent: TreeNode | None = parent
        self.children: list[TreeNode] = []

    def _add_child(self, x: float, y: float):
        """
        Method that creates a new node, and adds it as a child of the current node
        """
        new_node: TreeNode = TreeNode(x, y, self)
        self.children.append(new_node)

    def extend(self, x: float, y: float, delta: float):
        """
        Method for implementing the RRT that extends the current node towards a given
        (x,y) position
        * x: Position's x coordinate
        * y: Position's y coordinate
        * delta: Maximum distance between the current node and the extension
        """
        distance: float = np.linalg.norm([self.x - x, self.y - y])  # type: ignore

        if distance < delta:
            self._add_child(x, y)
        else:
            x_limited = self.x + delta * (x - self.x) / distance
            y_limited = self.y + delta * (y - self.y) / distance
            self._add_child(x_limited, y_limited)


if __name__ == "__main__":
    sample_tree = Tree(0.0, 0.0)
    sample_tree.root.extend(3.0, 3.0, 2.0)
    sample_tree.root.extend(-1.0, 1.0, 2.0)
    sample_tree.root.extend(1.0, -1.0, 2.0)
    sample_tree.root.extend(-1.0, -1.0, 2.0)

    sample_tree.root.children[0].extend(2.0, 2.0, 2.0)

    sample_tree.print()
    sample_tree.plot()
