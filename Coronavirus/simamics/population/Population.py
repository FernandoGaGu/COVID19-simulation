"""
*************************************************************************************************
***********************************// POPULATION MODULE //***************************************
*************************************************************************************************
In this module the population is defined. This population is made up of a series of individuals which
may have a disease state and be or not diagnosed.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
import random
from copy import deepcopy
from . import Individual
from ..states import *


class Population:
    """
    Class that represents a population made up of individuals.

    Attributes
    ------------
    space : int
        Space where population lives.

    deaths : int
        Number of deaths individuals.

    previousPopulation : int
        Population size from n-1 interaction.

    population: list
        List of individuals.
    """
    def __init__(self, initialCases, populationSize, space):
        """
        A population has a series of initial cases, a size and a space where individuals live.

        Parameters
        --------------
        :param initialCases: int
            Number of initial cases.
        :param populationSize:
            Initial population size.
        :param space:
            Space where the population lives.
        """
        self.space = space
        self.deaths = 0
        self.previousPopulation = populationSize
        # Initialize a fully healthy population
        healthy = Healthy()
        self.population = [Individual(deepcopy(healthy)) for n in range(populationSize)]
        # Introduce initial cases (only SymptomaticLight)
        for n in range(initialCases):
            infected = SymptomaticLight()
            self.population[n].state = infected
        random.shuffle(self.population)

    @property
    def numInfected(self):
        """
        Return the number of infected individuals in population.

        Return
        ----------
        :return: int
            Number of infected individuals in population.
        """
        numInfected = 0
        for individual in self.population:
            if individual.state == Infected():
                numInfected += 1

        return numInfected

    @property
    def numImmunized(self):
        """
        Return the number of immunized individuals (recovered) in population

        Return
        ---------
        :return: int
            Number of individuals immunized (recovered).
        """
        numImmunized = 0
        for individual in self.population:
            if isinstance(individual.state, Immunized):
                numImmunized += 1

        return numImmunized

    @property
    def infectedWithoutDiagnosis(self):
        """
        Return the number of infected individuals in population without diagnosis.

        Return
        ----------
        :return: int
            Number of individuals without diagnosed in population.
        """
        numInfectedWithoutDiagnosis = 0
        for individual in self.population:
            if individual.state == Infected() and not individual.diagnosed:
                numInfectedWithoutDiagnosis += 1

        return numInfectedWithoutDiagnosis

    def remove(self, idx):
        """
        Function that eliminate an individual from population because they are death.

        Parameter
        ------------
        :param idx: int
            Death individual index in population.
        """
        self.population.pop(idx)
        self.deaths += 1

