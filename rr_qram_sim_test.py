#############################################################
# rr_qram_sim_test.py
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

    # the sum of yield
    sum_of_yield: float = 0.0

    # simulator initialization
    rr_qram_sim: RRQramSim = RRQramSim('config.ini')

    # print out the simulator's configuration
    rr_qram_sim.print_config()

    for i in range(num_iter):
        # simulate error on the qrams
        num_faulty_qram = rr_qram_sim.simulate_error(num_qram)

        # yield calculation
        yield_qram: float = (num_qram - num_faulty_qram) / num_qram * 100.0
        sum_of_yield += yield_qram

        # just for debugging
        print('[{0:02d}] Yield (%): {1:5.2f}'.format(i, yield_qram))

    # average yield of the repeated simulations
    print('>> Average yield (%): {0:5.2f}'.format(sum_of_yield/num_iter))
