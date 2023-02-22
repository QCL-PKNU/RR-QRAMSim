#############################################################
# rr_qram_sim.py
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
from rr_qram import RRQram

#############################################################
# RRQramSim class
#############################################################

class RRQramSim:

    ##
    # Constructor of RRQramSim class
    #
    # @param self this object
    # @param path file path of the configuration file
    #
    def __init__(self, path: str):

        # RR-QRAMs to be simulated
        self.rr_qram_list = []

        # default configuration of the QRAM simulation
        # config['DEFAULT'] = {
        #     'dq_num' : '16',
        #     'rq_num' : '2',
        #     'dq_qec_npq' : 17
        #     'rq_qec_npq' : 17
        #     'dq_qec_dist' : 3
        #     'rq_qec_dist' : 3
        #     'dq_err_rate' : 0.005
        #     'rq_err_rate' : 0.005
        # }
        self.config = ConfigParser()
        self.config.read(path)

        # default configuration of the QRAM simulation
        default_config = self.config['DEFAULT']

        # the number of data and redundant qubits
        self.config.dq_num = int(default_config['dq_num'])
        self.config.rq_num = int(default_config['rq_num'])

        # the number of physical qubits of the data and redundant qubits
        self.config.dq_qec_npq = int(default_config['dq_qec_npq'])
        self.config.rq_qec_npq = int(default_config['rq_qec_npq'])

        # QEC distance of data and redundant qubits
        self.config.dq_qec_dist = int(default_config['dq_qec_dist'])
        self.config.rq_qec_dist = int(default_config['rq_qec_dist'])

        # fabrication error rate of data and redundant qubits
        self.config.dq_err_rate = float(default_config['dq_err_rate'])
        self.config.rq_err_rate = float(default_config['rq_err_rate'])

        # QEC model of data and redundant qubits
        self.config.dq_qec_model = QecModel(self.config.dq_qec_npq, self.config.dq_qec_dist)
        self.config.rq_qec_model = QecModel(self.config.rq_qec_npq, self.config.rq_qec_dist)

    ##
    # Destructor of RRQramSim class
    #
    # @param self this object
    #
    def __del__(self):
        del self.rr_qram_list

    ##
    # This is a function to simulate the error occurrence on the QRAMs at a given error rate.
    #
    # @param self this object
    # @param num_qrams the number of QRAMs to be simulated
    # @return the number of faulty QRAMs
    #
    def simulate_error(self, num_qrams: int):

        # the number of QRAMs not to be repaired
        num_faulty_qram: int = 0

        # RR-QRAM simulation
        self.rr_qram_list.clear()

        for i in range(num_qrams):
            # RR-QRAM initialization
            qram: RRQram = RRQram(self.config)
            self.rr_qram_list.append(qram)

            # error simulation on the RR-QRAM
            if qram.simulate_error(self.config.dq_err_rate, self.config.rq_err_rate):
                num_faulty_qram += 1

        return num_faulty_qram

    ##
    # This is a function to read a configuration file for initializing the RR-QRAM.
    #
    # @param self this object
    # @param num_qrams the number of QRAMs to be simulated
    # @return the number of faulty QRAMs
    #

    ##
    # This is a function to print out the brief configuration of the simulated RR-QRAM.
    #
    # @param self this object
    #
    def print_config(self):

        # print out the simulation configuration briefly
        dq_num = self.config.dq_num
        rq_num = self.config.rq_num

        dq_qec_npq = self.config.dq_qec_npq
        rq_qec_npq = self.config.rq_qec_npq

        # total number of physical qubits
        total_pq_num = dq_num * dq_qec_npq + rq_num * rq_qec_npq

        print('1) QEC Dist.(Size) of Data Qubits: {0} ({1})'.format(self.config.dq_qec_dist, dq_qec_npq))
        print('2) QEC Dist.(Size) of Redundant Qubits: {0} ({1})'.format(self.config.rq_qec_dist, rq_qec_npq))
        print('3) Number of Data Qubits: ', dq_num)
        print('4) Number of Redundant Qubits: ', rq_num)
        print('5) Error Rate of Data Qubits: ', self.config.dq_err_rate)
        print('6) Error Rate of Redundant Qubits: ', self.config.rq_err_rate)
        print('7) Total Number of Physical Qubits (QEC Size x # Logical Qubits): ', total_pq_num)
        print()

    ##
    # This is a debugging function to return the information of the QRAM simulation as a string format.
    #
    # @param self this object
    #
    def __str__(self):
        str_buf: str = ''

        qram_list = self.rr_qram_list
        for i in range(len(qram_list)):
            str_buf += '>> QRAM - {0:04d} ({1})\n'.format(i, ('Faulty' if qram_list[i].fault_state else 'Not faulty'))
            str_buf += str(qram_list[i]) + '\n'

        return str_buf

