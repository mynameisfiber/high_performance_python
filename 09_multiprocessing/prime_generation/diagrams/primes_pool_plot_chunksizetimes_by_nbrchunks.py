import math
import argparse
import random
import cPickle
import time
import multiprocessing
from matplotlib import pyplot as plt


def check_prime(n):
    if n % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument(
        '--create_data',
        action="store_true",
        default=False,
        help='if present then calculate data, if absent then plot')
    parser.add_argument(
        '--shuffle',
        action="store_true",
        default=False,
        help='randomly shuffle the job sequence')
    args = parser.parse_args()

    number_range = range(100000000, 100100000)  # B
    shuffle_in_filename = ""
    if args.shuffle:
        print "Shuffling..."
        shuffle_in_filename = "_shuffled"
        random.shuffle(number_range)

    filename = "primes_pool_plot_chunksizetimes_by_nbrchunks{}.pickle".format(
        shuffle_in_filename)
    png_filename = "08_primes_pool_plot_chunksizetimes_by_nbrchunks_sawtoothpattern{}.png".format(
        shuffle_in_filename)

    if args.create_data:
        NBR_PROCESSES = 4

        primes = []
        pool = multiprocessing.Pool(processes=NBR_PROCESSES)
        time_per_chunksize = []
        # plot the main effect:
        nbr_chunks_per_trial = range(1, 33)

        for nbr_chunks in nbr_chunks_per_trial:
            min_time = 99999999
            # run a number of trials and pick the fastest to avoid jitter
            for trial in xrange(10):
                t1 = time.time()
                chunksize = int(float(len(number_range)) / nbr_chunks)
                print nbr_chunks, chunksize

                pool.map(check_prime, number_range, chunksize=chunksize)
                t2 = time.time()
                min_time = min(t2 - t1, min_time)
            time_per_chunksize.append(min_time)
        cPickle.dump((nbr_chunks_per_trial, time_per_chunksize,
                      NBR_PROCESSES, number_range), open(filename, 'wb'))
    else:
        nbr_chunks_per_trial, time_per_chunksize, NBR_PROCESSES, number_range = cPickle.load(
            open(filename))
        # make a figure, show the experimental timings
        f = plt.figure(1)
        plt.clf()
        plt.plot(nbr_chunks_per_trial, time_per_chunksize,
                 "bx-", label="experiments")
        ax = f.get_axes()[0]

        # annotate the timings
        for nbr_chunks, time_cost in zip(nbr_chunks_per_trial, time_per_chunksize):
            ax.annotate('{:0.2f}s'.format(time_cost),
                        xy=(nbr_chunks, time_cost),
                        xytext=(5, 5),
                        ha='right',
                        textcoords='offset points',
                        fontsize='large')

        plt.ylabel("Completion time (seconds)")
        plt.xlabel("Number of chunks")
        plt.legend(numpoints=1, framealpha=0.9)
        plt.title(
            "Time cost of varying number of chunks with {} processes for\nprime checking in range [{}-{}]".format(
                NBR_PROCESSES,
                min(number_range),
                max(number_range)))
        plt.tight_layout()
        plt.savefig(png_filename)
