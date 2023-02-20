#############################################################
# physical_qubit.py
#
# Created: 2023. 01. 30
#
# Authors:
#    Dongmin Kim (kdm902077@pukyong.ac.kr)
#    Youngsun Han (youngsun@pknu.ac.kr)
#
# Quantum Computing Laboratory (quantum.pknu.ac.kr)
#############################################################

import random

#############################################################
# PhysicalQubit class
#############################################################

class PhysicalQubit:
    ##
    # Constructor of PhysicalQubit class
    #
    # @param self this object
    #
    def __init__(self):

        # fault occurrence of a physical qubit
        self.fault_state = False

    ##
    # This is a function to simulate an error on a specific qubit with the given error rate.
    #
    # @param self this object
    # @param err_rate the given error rate
    # @return whether this physical qubit is faulty or not
    #
    def simulate_error(self, err_rate: float = 0.0):

        # fault occurrence with binomial random distribution
        self.fault_state = random.choices([0, 1], weights=[1-err_rate, err_rate])[0]
        return self.fault_state

    ##
    # This is a debugging function to return the error state of a physical qubit as a string format.
    #
    # @param self this object
    #
    def __str__(self):
        return 'O' if self.fault_state is False else 'X'
