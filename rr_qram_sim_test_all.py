#############################################################
# rr_qram_sim_test_all.py
#
# Created: 2023. 02. 20
#
# Authors:
#    Dongmin Kim (kdm902077@pukyong.ac.kr)
#    Youngsun Han (youngsun@pknu.ac.kr)
#
# Quantum Computing Laboratory (quantum.pknu.ac.kr)
#############################################################

from rr_qram_sim import RRQramSim

#############################################################
# Main for the RR-QRAM simulator
#############################################################

if __name__ == '__main__':

    # number of iteration for obtaining the average yield
    num_iter: int = 10

    # number of QRAMs to be simulated
    num_qram: int = 1000

    # simulator initialization
    rr_qram_sim: RRQramSim = RRQramSim('config.ini')

    # the list of the numbers of data qubits
    dq_num_list = [16, 32, 64, 128, 256, 512, 1024]

    # the list of the error rates
    dq_ber_list = [0.005, 0.006, 0.007, 0.008, 0.009, 0.010]

    # the list of the numbers of spare qubits
    rq_num_list = [0, 1, 2, 4, 8]

    for rq_num in rq_num_list:
        # update the number of redundant qubits
        rr_qram_sim.config.rq_num = rq_num

        for err_rate in dq_ber_list:
            # update the error rate
            rr_qram_sim.config.dq_err_rate = err_rate
            rr_qram_sim.config.rq_err_rate = err_rate

            for dq_num in dq_num_list:
                # update the number of data qubits
                rr_qram_sim.config.dq_num = dq_num

                # print out the simulator's configuration
                rr_qram_sim.print_config()

                # the sum of yield
                sum_of_yield: float = 0.0

                for i in range(num_iter):
                    # simulate error on the qrams
                    num_faulty_qram = rr_qram_sim.simulate_error(num_qram)

                    # yield calculation
                    yield_qram: float = (num_qram - num_faulty_qram) / num_qram * 100.0
                    sum_of_yield += yield_qram

                    # just for debugging
                    print('[{0:02d}] Yield (%): {1:5.2f}'.format(i, yield_qram))

                # average yield of the repeated simulations
                print('>> Average yield (%): {0:5.2f}\n'.format(sum_of_yield/num_iter))
