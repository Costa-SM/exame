# polygon.py
# Author: João Lucas
# Created: 23.11.2024

import matplotlib.pyplot as plt

from rrt_methods.obstacles.obstacle import Obstacle


class Polygon(Obstacle):

    def __init__(self, xs: list[float], ys: list[float]) -> None:
        """
        Class that represents a polygon obstacle
        * xs: list of x coordinates of the polygon's contour
        * ys: list of y coordinates of the polygon's contour
        """
        self.xys = list(zip(xs, ys))

    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """Plots the polygon in the figure"""
        ax.add_patch(
            plt.Polygon(
                self.xys,
                facecolor="blue",
                edgecolor="black",
            )
        )

    def __main__():
        fig, ax = plt.subplots()
        ax.set_title("Polygon")
        polygon = Polygon([-5, -5, 5, 5], [-5, 5, 5, -5])
        polygon.plot(fig, ax)
        ax.autoscale_view()
        plt.show()


if __name__ == "__main__":
    Polygon.__main__()
