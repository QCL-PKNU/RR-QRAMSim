#############################################################
# qec_model.py
#
# Created: 2023. 01. 30
#
# Authors:
#    Dongmin Kim (kdm902077@pukyong.ac.kr)
#    Youngsun Han (youngsun@pknu.ac.kr)
#
# Quantum Computing Laboratory (quantum.pknu.ac.kr)
#############################################################

import math

#############################################################
# QecModel class
#############################################################

class QecModel:
    ##
    # Constructor of QecModel class
    #
    # @param self this object
    # @param pq_num the number of physical qubits
    # @param qec_dist the distance of the QEC
    #
    def __init__(self, pq_num: int, qec_dist: int):

        # the number of physical qubits
        self.pq_num: int = pq_num

        # parameters of the QEC model
        self.qec_dist: int = qec_dist                # distance
        self.qec_nrec: int = math.floor(qec_dist/2)  # number of repairable physical qubits

    ##
    # This is a debugging function to return the information of the QEC model as a string format.
    #
    # @param self this object
    #
    def __str__(self):
        str_buf: str = '>> QEC Model\n'
        str_buf += '1. QEC distance: {}\n'.format(self.qec_dist)
        str_buf += '2. # of physical qubits: {}\n'.format(self.pq_num)
        str_buf += '3. # of repairable qubits: {}\n'.format(self.qec_nrec)
        return str_buf
