"""Graph execution time for serial, threaded and processes forms of Pi estimation with numpy"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
# pi_numpy_serial_blocks.py
# (serial.py - same as serial blocks but for 1 large array only)
# pi_numpy_parallel_worker.py
speeds = np.array([[6.4, 6.4, 6.4, 6.4],
                   [6.4, 5.6, 5.3, 5.1],
                   [6.4, 3.2, 1.7, 1.5]])

nbr_cores = np.array([[1, 1, 1, 1],
                      [1, 2, 4, 8],
                      [1, 2, 4, 8]])

labels = np.array(["Series", "Threads", "Processes"])

plt.figure(1)
plt.clf()
markers = ['-.x', '--x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2)
plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(1, 7)
plt.xlim(0.5, 8.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title(
    "Time to estimate Pi using numpy with 100,000,000\ndart throws in series, threaded and with processes")
# plt.grid()
# plt.show()
plt.tight_layout()
plt.savefig("08_pi_numpy_graph_speed_tests_threaded_processes.png")
