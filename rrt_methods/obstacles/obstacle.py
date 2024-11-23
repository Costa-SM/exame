# obstacle.py
# Author: João Lucas
# Created: 23.11.2024

import matplotlib.pyplot as plt

from abc import ABC, abstractmethod


class Obstacle(ABC):

    @abstractmethod
    def __init__(self) -> None:
        """Abstract class that represents an obstacle"""
        raise NotImplementedError()

    @abstractmethod
    def plot(self, fig: plt.Figure, ax: plt.Axes) -> None:
        """Plots the obstacle in the figure"""
        raise NotImplementedError()

    @staticmethod
    def __main__():
        pass


if __name__ == "__main__":
    Obstacle.__main__()
