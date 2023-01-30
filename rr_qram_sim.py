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

from multiprocessing import Process, Manager
from configparser import ConfigParser
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
        self.__config = ConfigParser()
        self.__config.read(path)

    ##
    # Destructor of RRQramSim class
    #
    # @param self this object
    #
    def __del__(self):
        del self.rr_qram_list

    ##
    # This is a function to read a configuration file for initializing the RR-QRAM.
    #
    # @param self this object
    # @param num_qrams the number of QRAMs to be simulated
    # @return the number of faulty QRAMs
    #
    def simulate_error(self, num_qrams: int):

        # default configuration of the QRAM simulation
        default_config = self.__config['DEFAULT']

        # fabrication error rate of data and redundant qubits
        dq_err_rate: float = float(default_config['dq_err_rate'])
        rq_err_rate: float = float(default_config['rq_err_rate'])

        # the number of QRAMs not to be repaired
        num_faulty_qram: int = 0

        # RR-QRAM simulation
        self.rr_qram_list.clear()

        for i in range(num_qrams):
            # RR-QRAM initialization
            qram: RRQram = RRQram(self.__config)
            self.rr_qram_list.append(qram)

            # error simulation on the RR-QRAM
            if qram.simulate_error(dq_err_rate, rq_err_rate):
                num_faulty_qram += 1

        return num_faulty_qram

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

if __name__ == '__main__':

    # number of iteration for obtaining the average yield
    num_iter: int = 10

    # number of QRAMs to be simulated
    num_qram: int = 1000

    # the sum of yield
    sum_of_yield: float = 0.0

    for i in range(num_iter):
        # simulator initialization
        rr_qram_sim: RRQramSim = RRQramSim('config.ini')

        # simulate error on the qrams
        num_faulty_qram = rr_qram_sim.simulate_error(num_qram)

        # yield calculation
        yield_qram: float = (num_qram - num_faulty_qram) / num_qram * 100.0
        sum_of_yield += yield_qram

        # just for debugging
        print('[{0:02d}] Yield: {1:5.2f}%'.format(i, yield_qram))
        #print(rr_qram_sim)

        # delete the previous QRAM simulation
        del rr_qram_sim

    print('>> Average yield: {0:5.2f}%'.format(sum_of_yield/num_iter))
