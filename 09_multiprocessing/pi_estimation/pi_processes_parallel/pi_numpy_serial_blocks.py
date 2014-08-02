"""Estimate Pi using blocks of serial work on 1 CPU"""
import time
#from multiprocessing.dummy import Pool
import numpy as np


def estimate_nbr_points_in_circle(nbr_samples):
    # set random seed for numpy in each new process
    # else the fork will mean they all share the same state
    np.random.seed()
    xs = np.random.uniform(0, 1, nbr_samples)
    ys = np.random.uniform(0, 1, nbr_samples)
    estimate_inside_quarter_unit_circle = (xs * xs + ys * ys) <= 1
    nbr_trials_in_quarter_unit_circle = np.sum(
        estimate_inside_quarter_unit_circle)
    return nbr_trials_in_quarter_unit_circle


if __name__ == "__main__":
    nbr_samples_in_total = 1e8

    nbr_parallel_blocks = 4
    nbr_samples_per_worker = nbr_samples_in_total / nbr_parallel_blocks
    print "Making {} samples per worker".format(nbr_samples_per_worker)

    t1 = time.time()
    nbr_in_circle = 0
    for npb in xrange(nbr_parallel_blocks):
        nbr_in_circle += estimate_nbr_points_in_circle(nbr_samples_per_worker)
    print "Took {}s".format(time.time() - t1)
    pi_estimate = float(nbr_in_circle) / nbr_samples_in_total * 4
    print "Estimated pi", pi_estimate
    print "Pi", np.pi
