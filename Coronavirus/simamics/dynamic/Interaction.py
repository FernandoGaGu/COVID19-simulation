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

from .InteractionBase import InteractionBase
from math import *


class Interaction(InteractionBase):
    """
    This class define a function that model the number of interactions that occur
    in the population based on population size, population activity and space.
    """
    def __init__(self, expression):
        """
        The defined function must receive three parameters. The first parameter corresponds to
        the population size (of the integer type), the second to the percentage of activity
        of the population (of the float type) and the last to the space where the population
        lives (of the integer type). All three must be denoted by size, mov and space
        respectively. See pre-built-functions.info for examples.

        :param expression: lambda
            Function that define the number of interactions that the population can have.
        """
        self.definition = expression

    def interactions(self, size: int, mov: float, space: int):
        """
        Function that receives three parameters and return an integer that define the number
        of interaction.

        Parameters
        -------------
        :param size: int
            Population size.
        :param mov: float
            Population activity.
        :param space: int
            Population space

        Return
        --------
        :return: int
            Number of interactions.
        """
        return self.definition(size, mov, space)

    def plotFunction(self, **kwargs):
        """
        Function that plot the function in 3D.

        :param kwargs:
            See InteractionBase
        """
        super().plotFunction(self.definition,  **kwargs)