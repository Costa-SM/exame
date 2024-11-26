# obstacle.py
# Author: João Lucas
# Created: 23.11.2024

from __future__ import annotations

import matplotlib.pyplot as plt

from abc import ABC, abstractmethod


class Obstacle(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """
        Abstract class that represents an obstacle
        """
        raise NotImplementedError()

    @abstractmethod
    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """
        Plots the obstacle in the figure
        * fig: pyplot's figure
        * ax: pyplot's axes (1 axis)
        """
        raise NotImplementedError()

    @abstractmethod
    def distance(self, point: tuple[float, float]) -> float:
        """
        Calculates a point's distance to the obstacle
        * point: x and y coordinates of the point
        """
        raise NotImplementedError()

    @staticmethod
    def __main__():
        raise NotImplementedError()


if __name__ == "__main__":
    Obstacle.__main__()
