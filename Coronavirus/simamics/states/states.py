"""
*************************************************************************************************
*************************************// STATES MODULE //*****************************************
*************************************************************************************************

In this module the possible states of the population are defined. An individual may be
healthy or ill. An healthy individual can be immune or not. Infected patients can have different
stages of disease.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
from abc import ABCMeta


class State:
    """
    Class that defines conceptually what a state is.
    """
    __metaclass__ = ABCMeta


class Healthy(State):
    """
    A healthy individual is who is not infected.
    """
    def __init__(self):
        """
        The interaction capacity of a healthy individual is 100%.
        """
        self.interactionCapacity = 1

    def __repr__(self):
        return "Healthy"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return True


class Infected(State):
    """
    An infected individual is who has been affected by the pathogen.
    """
    def __init__(self):
        """
        The infected individuals count the days they remain infected before being immunized
        """
        self.daysWithInfection = 0

    def __repr__(self):
        return "Infected"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return True


class Asymptomatic(Infected):
    """
    Infected individual without symptoms.
    """
    def __init__(self):
        """
        The interaction capacity of asymptomatic individuals is the same as healthy individuals.
        Also they count the days before being immunized. Until then, they can transmit the pathogen.
        """
        super().__init__()
        self.interactionCapacity = 1

    def __repr__(self):
        return "Asymptomatic"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return super().__eq__(other)
        return True


class SymptomaticLight(Infected):
    """
    Infected individual with light symptoms.
    """
    def __init__(self):
        """
        The interaction capacity with other individuals is less than healthy or asymptomatic
        people.
        """
        super().__init__()
        self.interactionCapacity = 0.7

    def __repr__(self):
        return "Symptomatic Light"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return super().__eq__(other)
        return True


class SymptomaticMild(Infected):
    """
    Infected individual with mild symptoms.
    """
    def __init__(self):
        """
        The interaction capacity is low.
        """
        super().__init__()
        self.interactionCapacity = 0.3

    def __repr__(self):
        return "Symptomatic Mild"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return super().__eq__(other)
        return True


class SymptomaticSevere(Infected):
    """
    Infected individual with severe symptoms.
    """
    def __init__(self):
        """
        The interaction capacity of this individuals is very low.
        """
        super().__init__()
        self.interactionCapacity = 0.1

    def __repr__(self):
        return "Symptomatic Severe"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return super().__eq__(other)
        return True


class Immunized(State):
    """
    Individual that has passed the infection and cannot be infected again.
    """
    def __init__(self):
        """
        Their interaction capacity is the same as healthy individuals.
        """
        self.interactionCapacity = 1

    def __repr__(self):
        return "Immunized"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if not isinstance(other, __class__):
            return False
        return True
