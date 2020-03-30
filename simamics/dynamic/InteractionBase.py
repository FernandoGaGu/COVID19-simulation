"""
*************************************************************************************************
**********************************// VISUALIZATION MODULE //*************************************
*************************************************************************************************
This module provides the basic tools for simulation. Using the Interaction class is possible to define
a function that model the number of interactions that occur in the population. This function is based
on the variables following variables: population size, population activity and space.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
from abc import ABCMeta, abstractmethod


class InteractionBase:
    """
    Abstract class that defines the interface to define an interaction. See Interaction for
    detailed description.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def interactions(self, size: int, mov: float, space: int):
        """
        Function that receives three parameters and return an integer that define the number
        of interaction.

        Attributes
        -------------
        :param size: int
            Population size.
        :param mov: float
            Population activity.
        :param space: float
            Population space.

        Return
        --------
        :return: int
            Number of interactions.
        """
        pass

    def plotFunction(self, function, **kwargs):
        """
        This method allows to represent the expression in a three-dimensional graph.
        The space parameter must be a fixed number, the population size and movement rate can
        be multidimensional arrays. This function has as default parameters a population size
        ranging from 100 to 1000 and a space of 400.

        Parameters
        ------------
        :param function: function
            Function to generate the number of interactions.
        :param populationSize: <optional> np.ndarray
            Population sizes. Default np.array([x for x in range(1, 1000)])
        :param populationMovement: <optional> np.ndarray
            Population activity rates. Default np.linspace(0.01, 0.99, 999)
        :param populationSpace: <optional> int
            Population space. Default 400.
        """
        import numpy as np
        populationSize = kwargs.get('populationSize', np.array([x for x in range(1, 1000)]))
        populationMovement = kwargs.get('populationMovement', np.linspace(0.01, 0.99, 999))
        populationSpace = kwargs.get('populationSpace', 400)
        numOfInteractions = np.array([
            function(size, mov, populationSpace) for size, mov in zip(populationSize, populationMovement)
        ])
        self._plot(xAxis=populationSize, yAxis=numOfInteractions, zAxis=populationMovement)

    def _plot(self, xAxis: list, zAxis: list, yAxis: list):
        """
        Private function that performs the graphic representation.
        """
        from mpl_toolkits import mplot3d
        import matplotlib.pyplot as plt
        fig = plt.figure(figsize=(7, 5))
        ax = plt.axes(projection='3d')
        ax.plot3D(xAxis,zAxis, yAxis, 'red')
        ax.set_xlabel('Population size')
        ax.set_ylabel('Population movement')
        ax.set_zlabel('Number of interactions')
