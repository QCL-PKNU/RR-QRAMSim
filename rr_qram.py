#############################################################
# rr_qram.py
#
# Created: 2023. 01. 30
#
# Authors:
#    Dongmin Kim (kdm902077@pukyong.ac.kr)
#    Youngsun Han (youngsun@pknu.ac.kr)
#
# Quantum Computing Laboratory (quantum.pknu.ac.kr)
#############################################################

from configparser import ConfigParser
from qec_model import QecModel
from logical_qubit import LogicalQubit

#############################################################
# RRQram class
#############################################################

class RRQram:

    ##
    # Constructor of RRQram class
    #
    # @param self this object
    # @param config configuration of the qram
    def __init__(self, config: ConfigParser):

        # data and redundant qubits
        self.__dq_list = []
        self.__rq_list = []

        # default configuration
        default_config = config['DEFAULT']

        # the number of data and redundant qubits
        self.__dq_num = int(default_config['dq_num'])
        self.__rq_num = int(default_config['rq_num'])

        # the number of physical qubits of the data and redundant qubits
        self.__dq_qec_npq = int(default_config['dq_qec_npq'])
        self.__dq_qec_npq = int(default_config['rq_qec_npq'])

        # QEC distance of data and redundant qubits
        self.__dq_qec_dist = int(default_config['dq_qec_dist'])
        self.__rq_qec_dist = int(default_config['rq_qec_dist'])

        # QEC model of data and redundant qubits
        self.__dq_qec_model = QecModel(self.__dq_qec_npq, self.__dq_qec_dist)
        self.__rq_qec_model = QecModel(self.__dq_qec_npq, self.__rq_qec_dist)

        # initialize data and redundant qubits
        for i in range(self.__dq_num):
            self.__dq_list.append(LogicalQubit(self.__dq_qec_model))

        for i in range(self.__rq_num):
            self.__rq_list.append(LogicalQubit(self.__rq_qec_model))

        # fault occurrence of a logical qubit
        self.fault_state = False

    ##
    # Destructor of RRQram class
    #
    # @param self this object
    #
    def __del__(self):
        del self.__dq_list
        del self.__rq_list

    ##
    # This function simulates the error occurrence on the logical qubits of a QRAM.
    # at a given error rate. By referring to the QEC model, this returns the number of faulty logical qubits.
    #
    # @param self this object
    # @param dq_err_rate the fabrication error rate of physical qubits on data qubits
    # @param rq_err_rate the fabrication error rate of physical qubits on redundant qubits
    # @return whether this QRAM is faulty or not
    #
    def simulate_error(self, dq_err_rate: float, rq_err_rate: float):

        # the number of faulty data and redundant qubits
        num_dq_faults: int = 0
        num_rq_faults: int = 0

        # simulate error on data and redundant qubits at the given error rate
        for dq in self.__dq_list:
            # error simulation on data qubits
            if dq.simulate_error(dq_err_rate):
                num_dq_faults += 1

        for rq in self.__rq_list:
            # error simulation on redundant qubits
            if rq.simulate_error(rq_err_rate):
                num_rq_faults += 1

        # the number of data qubits to be repaired
        num_repairable = self.__rq_num - num_rq_faults

        # check the possibility of the recovery of the faulty QRAM
        self.fault_state = (num_dq_faults > num_repairable)
        return self.fault_state

    ##
    # This is a debugging function to return the information of the QRAM as a string format.
    #
    # @param self this object
    #
    def __str__(self):
        str_buf: str = ''

        for i in range(self.__dq_num):
            str_buf += '[{0:04d}] data {1}\n'.format(i, self.__dq_list[i])

        for i in range(self.__rq_num):
            str_buf += '[{0:04d}] redundant {1}\n'.format(i, self.__rq_list[i])

        return str_buf
