"""
*************************************************************************************************
**********************************// VISUALIZATION MODULE //*************************************
*************************************************************************************************
This module provides basic tools to visualize the simulation result.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
from ..population import Population
from ..states import *


class Report:
    """
    Class that records the parameters of evolution.

    Attributes
    ------------
    timeUnits : list
        Number of interactions in days.

    totalCases :  list
        Number of infected individuals in population.

    recovered : list
        Number of recovered individuals in population (accumulative).

    totalDetailedCases : list
        Dictionary with detailed information on the evolution of the simulation.

    diagnosed : list
        Number of diagnosed individuals in population.

    deaths : list
        Number of death individuals in population per iteration.

    Methods
    --------
    plotStatistics(): Plot all statistics.

    plotInfected(): Plot the number of infected per iteration (accumulated).

    plotDeaths(): Plot the number of deaths per iteration (accumulated).

    plotDiagnosedStatus(): Plot the number of diagnosed/Undiagnosed individuals
        per population (accumulated).
    """

    def __init__(self):
        self.timeUnits = []
        self.totalCases = []
        self.recovered = []
        self.totalDetailedCases = []
        self.diagnosed = []
        self.deaths = []

    @property
    def totalDeaths(self):
        """
        Return the total number of death individuals.

        Return
        ---------
        :return: int
            Number of death individuals.
        """
        return sum(self.deaths)

    def count(self, timeUnit: int, population: Population):
        """
        Record the population state.

        Parameters
        ------------
        :param timeUnit: int
            Iteration.
        :param population: simamics.population.Population
            Population.

        """
        detailedCases = {
            'healthy': 0, 'infLight': 0, 'infMild': 0, 'infSevere': 0, 'asymptomatic': 0, 'immunized': 0
        }

        for individual in population.population:
            if isinstance(individual.state, Healthy):
                detailedCases['healthy'] += 1
            elif isinstance(individual.state, SymptomaticLight):
                detailedCases['infLight'] += 1
            elif isinstance(individual.state, SymptomaticMild):
                detailedCases['infMild'] += 1
            elif isinstance(individual.state, SymptomaticSevere):
                detailedCases['infSevere'] += 1
            elif isinstance(individual.state, Asymptomatic):
                detailedCases['asymptomatic'] += 1
            else:
                detailedCases['immunized'] += 1
        # Save report
        self.timeUnits.append(timeUnit)
        self.totalCases.append(population.numInfected)
        self.totalDetailedCases.append(detailedCases)
        self.diagnosed.append(population.numInfected - population.infectedWithoutDiagnosis)
        self.recovered.append(population.numImmunized)

    def recordDeaths(self, numDeaths):
        """
        Record the number of deaths for a given iteration.

        Parameters
        ------------
        :param numDeaths: int
            Number of deaths in a given iteration
        """
        self.deaths.append(numDeaths)

    def plotStatistics(self, title="Pathogen infection"):
        """
        Plot simulation evolution.
        """
        self.__matplotlib(xAxis=self.timeUnits,
                          yAxis=[self.totalCases, self.deaths, self.recovered, self.diagnosed],
                          title=title,
                          color=['red', 'blue', 'green', 'yellow'],
                          marker=['.', 'o', '.', 'o'],
                          xlabel='Days',
                          ylabel='Total cases',
                          labels=['Real infections', 'Deaths', 'Recovered', 'Diagnosed'])

    def plotInfected(self, title="Pathogen infection"):
        """
        Plot number of infected individuals.
        """

        self.__matplotlib(xAxis=self.timeUnits, yAxis=[self.totalCases], title=title,
                          color=['red'], marker=['o'], xlabel='Days', ylabel='Total cases',
                          labels=['Infected'])

    def plotDeaths(self, title="Pathogen caused deaths"):
        """
        Plot the number of deaths
        """
        self.__matplotlib(xAxis=self.timeUnits, yAxis=[self.deaths], title=title,
                          color=['red'], marker=['o'], xlabel='Days', ylabel='Total deaths',
                          labels=['Deaths'])

    def plotDiagnosedStatus(self, title="Diagnosed/Undiagnosed cases"):
        """
        Plot the number of deaths
        """
        self.__matplotlib(xAxis=self.timeUnits, yAxis=[self.diagnosed, self.totalCases], title=title,
                          color=['green', 'red'], marker=['.','o'], xlabel='Days', ylabel='Total cases',
                          labels=['Diagnosed', 'Undiagnosed'])

    def __matplotlib(self, xAxis, yAxis, title, color, marker, xlabel, ylabel, labels):
        """
        Private function that make the representation.
        """
        import matplotlib.pyplot as plt
        # Add some days after epidemics start
        daysBefore = 10
        xDaysBefore = [-1 * x for x in range(1, daysBefore)][::-1]
        yDaysBefore = [0 for x in range(1, daysBefore)]
        xAxis = xDaysBefore + xAxis
        yAxis = [yDaysBefore + yAxisParams for yAxisParams in yAxis]
        # Make representation
        fig, ax = plt.subplots(figsize=(12, 10))
        for n in range(len(yAxis)):
            ax.plot(xAxis, yAxis[n], color=color[n], marker=marker[n], markersize=3, label=labels[n])
            ax.set_xlabel(xlabel[n])
            ax.set_ylabel(ylabel[n])
            ax.fill_between(xAxis, yAxis[n], 0, alpha=0.1, color=color[n])
        ax.legend()
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.title(title, fontsize='x-large')
        plt.show()
