# obstacle.py
# Author: Joao Lucas
# Created: 23.11.2024

from __future__ import annotations

from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
from matplotlib.axes import Axes


class Obstacle(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """
        Abstract class that represents an obstacle
        """
        raise NotImplementedError()

    @abstractmethod
    def plot(self, ax: Axes) -> None:
        """
        Plots the obstacle in the figure
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
