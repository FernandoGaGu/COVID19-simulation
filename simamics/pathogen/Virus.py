"""
*************************************************************************************************
**************************************// VIRUS MODULE //*****************************************
*************************************************************************************************
This module models the properties of a virus such as its half-life, percentage of death, different
percentage of cases and the percentage of transmission.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
from ..states.states import *
import random


class Virus:
    """
    Class that represent the virus

    Attributes
    -----------
    lifeTime : int
        Number of days the infection lasts.

    deathRate : float
        Virus lethality.

    lightPercentage : float
        Percentage of light cases.

    mildPercentage : float
        Percentage of mild cases.

    severePercentage : float
        Percentage of severe cases.

    asymptomaticPercentage : float
        Percentage of asymptomatic cases.

    transmissionPercentage : float
        Ability to infect new hosts.
    """

    def __init__(self, lifeTime: int, deathRate: float, lightPercentage: float, mildPercentage: float,
                 severePercentage: float, asymptomaticPercentage: float, transmissionPercentage: float):
        """
        Definition of some basic aspects of the virus such as its half-life, percentage of death,
        transmission capacity and percentage of each of the states that the virus can produce (must sum 1).

        Parameters
        ------------
        :param lifeTime: int
            Number of days the infection lasts.

        :param deathRate: float
            Virus lethality.

        :param lightPercentage: float
            Percentage of light cases.

        :param mildPercentage: float
            Percentage of mild cases.

        :param severePercentage: float
            Percentage of severe cases.

        :param asymptomaticPercentage: float
            Percentage of asymptomatic cases.

        :param transmissionPercentage: float
            Ability to infect new hosts.
        """
        self.lifeTime = lifeTime
        self.deathRate = deathRate
        self.lightPercentage = lightPercentage
        self.mildPercentage = self.lightPercentage + mildPercentage
        self.severePercentage = self.mildPercentage + severePercentage
        self.asymptomaticPercentage = self.severePercentage + asymptomaticPercentage
        self.transmissionPercentage = transmissionPercentage
        if (lightPercentage + severePercentage + mildPercentage + asymptomaticPercentage) != 1:
            raise TypeError("Percentages have to sum 1, instead mildPercentage + severePercentage"
                            " + asymptomaticPercentage sum %.2f" %
                            (lightPercentage + severePercentage + mildPercentage + asymptomaticPercentage))

    def __repr__(self):
        return "< Virus: life time: %d; death rage: %.2f; transmission percentage: %.2f; light: %.2f; mild: %.2f; " \
               "severe: %.2f; asymptomatic: %.2f" % (self.lifeTime, self.deathRate, self.transmissionPercentage,
                                                     self.lightPercentage, self.mildPercentage - self.lightPercentage,
                                                     self.severePercentage - self.mildPercentage,
                                                     1 - self.severePercentage)

    def __str__(self):
        return self.__repr__()

    @property
    def infect(self):
        """
        Function that determines if the infection occurs and the state in which the infected individual
        will be based on the parameters provided in their builder.

        Return
        ---------
        :return: coronvarius.states.State
            New individual state.
        """
        if random.uniform(1, 0) > self.transmissionPercentage:
            # The virus does not infect the individual
            return Healthy()
        randomNum = random.uniform(1, 0)
        if randomNum <= self.lightPercentage:
            # The virus infect the individual creating a light disease
            return SymptomaticLight()
        elif randomNum <= self.mildPercentage:
            # The virus infect the individual creating a mild disease
            return SymptomaticMild()
        elif randomNum <= self.severePercentage:
            # The virus infect the individual creating a severe disease
            return SymptomaticSevere()
        else:
            # The virus infect the individual creating a asymptomatic disease
            return Asymptomatic()
