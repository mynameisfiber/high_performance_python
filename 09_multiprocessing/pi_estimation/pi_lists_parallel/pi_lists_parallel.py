import random
import time
import argparse


def estimate_nbr_points_in_quarter_circle(nbr_estimates):
    nbr_trials_in_quarter_unit_circle = 0
    for step in xrange(int(nbr_estimates)):
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_quarter_unit_circle += is_in_unit_circle

    return nbr_trials_in_quarter_unit_circle


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument(
        'nbr_workers', type=int, help='Number of workers e.g. 1, 2, 4, 8')
    parser.add_argument(
        '--nbr_samples_in_total',
        type=int,
        default=1e8,
        help='Number of samples in total e.g. 100000000')
    parser.add_argument(
        '--processes',
        action="store_true",
        default=False,
        help='True if using Processes, absent (False) for Threads')

    args = parser.parse_args()
    if args.processes:
        print "Using Processes"
        from multiprocessing import Pool
    else:
        print "Using Threads"
        from multiprocessing.dummy import Pool

    nbr_samples_in_total = args.nbr_samples_in_total  # should be 1e8
    nbr_parallel_blocks = args.nbr_workers
    pool = Pool(processes=nbr_parallel_blocks)
    nbr_samples_per_worker = nbr_samples_in_total / nbr_parallel_blocks
    print "Making {} samples per {} worker".format(nbr_samples_per_worker, nbr_parallel_blocks)
    nbr_trials_per_process = [nbr_samples_per_worker] * nbr_parallel_blocks
    t1 = time.time()
    nbr_in_quarter_unit_circles = pool.map(
        estimate_nbr_points_in_quarter_circle, nbr_trials_per_process)
    pi_estimate = sum(nbr_in_quarter_unit_circles) * \
        4 / float(nbr_samples_in_total)
    print "Estimated pi", pi_estimate
    print "Delta:", time.time() - t1
