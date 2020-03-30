"""
*************************************************************************************************
***********************************// POPULATION MODULE //***************************************
*************************************************************************************************
In this module the population is defined. This population is made up of a series of individuals which
 may have a disease state and be or not diagnosed.

Author: Fernando García Gutiérrez
Email: fernando.garciagu@upm.es
"""
from ..states import State


class Individual:
    """
    Class that represent an individual.

    Attributes
    ------------
    state : coronavirus.states.State
        Individual state

    diagnosed : bool
        If the individual has been diagnosed or not.
    """
    def __init__(self, initialState):
        """
        An individual need an initial state.

        Parameters
        ------------
        :param initialState: simamics.states.State
            Individual initial state.
        """
        self._state = initialState
        self.diagnosed = False

    def __repr__(self):
        return "< Individual, State: %s >" % self.state

    def __str__(self):
        return self.__repr__()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, newState):
        """
        Change individual state. Setter method.

        Parameter
        -----------
        :param newState: simamics.states.State
            New individual state.
        """
        self._state = newState




