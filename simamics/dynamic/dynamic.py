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
import random
from tqdm import tqdm
from ..visualization import Report
from ..population import Population, Individual
from ..pathogen import Virus
from ..states import *
from .InteractionBase import InteractionBase


def _infect(individual: Individual, virus: Virus):
    """
    Function that infect an individual using a virus.

    Parameters
    ------------
    :param individual: simamics.popualtion.Individual
        Individual
    :param virus: simamics.pathogen.Virus
        Virus.

    Return
    -------
    :return: simamics.popualtion.Individual
        Individual
    """
    # If the individual has passed the infection or is infected they cannot be infected again
    if not isinstance(individual.state, Immunized) and not individual.state == Infected():
        individual.state = virus.infect

    return individual


def _kill(population: Population, virus: Virus):
    """
    Function that kill severe individuals based on virus death rate.

    Parameters
    -------------
    :param population: simamics.popualtion.Population
        Population.
    :param virus:  simamics.pathogen.Virus
        Virus

    Return
    ---------
    :return: int
        Number of death individuals.
    """
    deathIndividuals = 0
    for n, individual in enumerate(population.population):
        if individual.state == SymptomaticSevere():
            if virus.deathRate >= random.uniform(0, 1):
                # Remove individual from population
                population.remove(n)
                deathIndividuals += 1
    return deathIndividuals


def _generateInteractions(population: Population, virus: Virus, populationActivity: float, interaction):
    """
    Function that simulates the interactions between individuals in the population.

    Parameters
    ------------
    :param interaction: Interaction
        Interaction.
    :param virus: simamics.pathogen.Virus
        Virus.
    :param population: simamics.population.Population
        Population.
    :param populationActivity: float
        Population activity.
    """
    numOfInteractions = interaction.interactions(len(population.population), populationActivity, population.space)
    for n in range(numOfInteractions):
        for individual in population.population:
            # Probability of two individuals interact
            randomIndividual = random.randrange(0, len(population.population))
            interactionProb = individual.state.interactionCapacity * \
                              population.population[randomIndividual].state.interactionCapacity

            if interactionProb > random.uniform(0, 1):
                if population.population[randomIndividual].state == Infected() and individual == Healthy():
                    # Individual if infected by random individual in population
                    _infect(individual, virus)
                elif individual.state == Infected() and population.population[randomIndividual].state == Healthy():
                    # Random individual is infected by individual
                    _infect(population.population[randomIndividual], virus)


def _increment(population: Population, virusLifeTime: int):
    """
    Function that advances the number of days that patients have been infected.

    Parameters
    -------------
    :param virusLifeTime: int
        Virus life time.
    :param population: simamics.population.Population
        Population.
    """
    for individual in population.population:
        if individual.state == Infected():
            individual.state.daysWithInfection += 1
            if individual.state.daysWithInfection > virusLifeTime:
                individual.state = Immunized()


def _diagnosingPopulation(population: Population, diagnosisPercentage: float):
    """
    Function that performs the diagnosis. If the individual is diagnosed their mobility is
    drastically reduced to 0.05.

    Parameters
    ------------
    :param population: simamics.population.Population
        Population
    :param diagnosisPercentage: float
        Percentage of test.
    """
    numberOfTest = int(diagnosisPercentage * population.infectedWithoutDiagnosis)
    totalDiagnosed = 0
    for individual in population.population:
        if individual.diagnosed:
            continue
        if isinstance(individual.state, SymptomaticLight) or isinstance(individual.state, SymptomaticMild) \
                or isinstance(individual.state, SymptomaticSevere):
            # Diagnosed individual
            individual.diagnosed = True
            # Reduce the interaction capacity
            individual.state.interactionCapacity = 0.01
            numberOfTest -= 1
            totalDiagnosed += 1
        if numberOfTest == 0:
            break


def simulate(population: Population, virus: Virus, iterations: int, populationActivity: float,
             diagnosisPercentage: float, interaction: InteractionBase):
    """
    Function that simulate the virus dynamic for a given population and for a given number of interactions,
    taking into account the virus parameters (see simamics.pathogen.Virus), the percentage of diagnosed
    individuals in population and the population activity.

    Parameters
    ------------
    :param diagnosisPercentage: float
        Percentage of test (see _diagnosingPopulation for a detailed implementation).
    :param interaction: Interaction
        Interaction function (see Interaction for a detailed implementation).
    :param population: simamics.population.Population
        Population.
    :param virus: simamics.pathogen.Virus
        Virus.
    :param iterations: int
        Number of simulation interactions.
    :param populationActivity: float
        Population activity.

    Return
    ---------
    :return: simamics.visualization.Report
        Report instance (see simamics.visualization.Report for a detailed description)
    """
    if not isinstance(population, Population):
        raise TypeError("You must define a population using Population package")
    if not isinstance(virus, Virus):
        raise TypeError("You must define a virus using Virus package")
    if not isinstance(interaction, InteractionBase):
        raise TypeError("You must define an interaction using Interaction package "
                        "or pre-built functions from PreBuiltFunctions package")

    report = Report()
    for i in tqdm(range(iterations), desc="Days %d" % iterations):
        report.count(i, population)
        _diagnosingPopulation(population, diagnosisPercentage)
        _generateInteractions(population, virus, populationActivity, interaction)
        numDeaths = _kill(population, virus)
        report.recordDeaths(numDeaths)
        _increment(population, virus.lifeTime)

    return report
