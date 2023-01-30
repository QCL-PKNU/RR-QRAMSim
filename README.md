# RR-QRAMSim
A simulator for redundant repair of QRAM

1. You need to configure the following configuration file before the estimation: config.ini.

<pre>
<code>
  # The number of data qubits in a QRAM 
  dq_num = 128

  # The number of redundant qubits in a QRAM 
  rq_num = 1

  # The number of physical qubits of a data qubit 
  dq_qec_npq = 17

  # The number of physical qubits of a redundant qubit 
  rq_qec_npq = 17

  # The code distance for a data qubit 
  dq_qec_dist = 3

  # The code distance for a redundant qubit 
  rq_qec_dist = 3

  # The error rate applied to a data qubit 
  dq_err_rate = 0.01

  # The error rate applied to a redundant qubit 
  rq_err_rate = 0.01
</code>
</pre>

2. You can modify the number of iterations and the QRAMs to be simulated: rr_qram_sim.py.

<pre>
<code>
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
</code>
</pre>
