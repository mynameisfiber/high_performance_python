"""Graph execution time for serial, threaded and processes forms of Pi estimation with lists"""
import numpy as np
import matplotlib.pyplot as plt

# timings generated using
#  pi_lists_parallel
speeds = np.array([[110.0],
                   [118.0, 144.0, 149.0, 150.0],
                   [110.0, 55.0, 28.0, 27.0]])

nbr_cores = np.array([[1],
                      [1, 2, 4, 8],
                      [1, 2, 4, 8]])

labels = np.array(["Series", "Threads", "Processes"])

plt.figure(1)
plt.clf()
markers = ['-.o', '--x', '-x']
for nc, sp, label, mk in zip(nbr_cores, speeds, labels, markers):
    plt.plot(nc, sp, mk, label=label, linewidth=2)
plt.annotate("Series and 1 Process have the same execution time",
             (nbr_cores[0][0] + 0.1, speeds[0][0]))
plt.legend(loc="lower left", framealpha=0.8)
plt.ylim(20, 155)
plt.xlim(0.5, 8.5)
plt.ylabel("Execution time (seconds) - smaller is better")
plt.xlabel("Number of workers")
plt.title(
    "Time to estimate Pi using objects with 100,000,000\ndart throws in series, threaded and with processes")
# plt.grid()
# plt.show()
plt.tight_layout()
plt.savefig("08_pi_lists_graph_speed_tests_threaded_processes.png")
