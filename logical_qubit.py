#############################################################
# logical_qubit.py
#
# Created: 2023. 01. 30
#
# Authors:
#    Dongmin Kim (kdm902077@pukyong.ac.kr)
#    Youngsun Han (youngsun@pknu.ac.kr)
#
# Quantum Computing Laboratory (quantum.pknu.ac.kr)
#############################################################

from qec_model import QecModel
from physcial_qubit import PhysicalQubit

#############################################################
# LogicalQubit class
#############################################################

class LogicalQubit:

    ##
    # Constructor of LogicalQubit class
    #
    # @param self this object
    # @param qec_model the error model of the logical qubit
    #
    def __init__(self, qec_model: QecModel):

        # the error model of the logical qubit
        self.__qec_model: QecModel = qec_model

        # physical qubits
        self.__pq_list: list = []

        # simulate the error occurrence on each physical qubit with the given error rate
        for i in range(qec_model.pq_num):
            self.__pq_list.append(PhysicalQubit())

        # fault occurrence of a logical qubit
        self.fault_state = False

    ##
    # Destructor of LogicalQubit class
    #
    # @param self this object
    #
    def __del__(self):
        del self.__pq_list

    ##
    #  This function simulates the error occurrence on the physical qubits of this logical qubit
    #  at a given error rate. By referring to the QEC model, this returns True
    #  if the logical qubit is faulty. Otherwise, returns False.
    #
    # @param self this object
    # @param err_rate the fabrication error rate of physical qubits
    # @return whether this logical qubit is faulty or not
    #
    def simulate_error(self, err_rate: float):

        # number of faults on physical qubits
        num_pq_faults = 0

        # simulate the error occurrence on each physical qubit with the given error rate
        for pq in self.__pq_list:
            if pq.simulate_error(err_rate):
                num_pq_faults += 1

        # return True if the fault number of physical qubits is greater than
        # the number of repairable physical qubits. otherwise, return False.
        self.fault_state = (num_pq_faults > self.__qec_model.qec_nrec)
        return self.fault_state

    ##
    # This is a debugging function to return the error states of the physical qubits as a string format.
    #
    # @param self this object
    #
    def __str__(self):
        str_buf: str = 'logical qubit: ['
        for pq in self.__pq_list:
            str_buf += ' {}'.format(str(pq))
        return str_buf + ' ]' + (' F' if self.fault_state else '')
