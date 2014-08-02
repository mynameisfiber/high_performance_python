import math
import random
import time
import argparse
import cPickle
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
    parser.add_argument('type', type=int, default=1, help='type 1 or 2')
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

    primes = []
    NBR_PROCESSES = 4
    pool = multiprocessing.Pool(processes=NBR_PROCESSES)

    number_range = range(100000000, 100100000)  # B
    shuffle_in_filename = ""
    if args.shuffle:
        print "Shuffling..."
        shuffle_in_filename = "shuffled_"
        random.shuffle(number_range)

    plot_type = args.type
    CREATE_DATA = args.create_data
    print args
    filename = "primes_pool_plot_chunksize_{}type{}.pickle".format(
        shuffle_in_filename, plot_type)
    png_filename = "08_primes_pool_plot_chunksizetimes_1to50000_{}plottype{}.png".format(
        shuffle_in_filename,
        plot_type)

    if CREATE_DATA:
        time_per_chunksize = []
        if plot_type == 1:
            # plot the main effect:
            chunksizes = [
                1, 2, 3, 4, 5, 8, 10, 50, 100, 1000, 5000, 10000, 50000]
        if plot_type == 2:
            chunksizes = [1, 2, 4, 8, 16, 32, 64]

        for chunksize in chunksizes:
            min_time = 99999999
            # run a number of trials and pick the fastest to avoid jitter
            for trial in xrange(10):
                t1 = time.time()
                pool.map(check_prime, number_range, chunksize=chunksize)
                t2 = time.time()
                min_time = min(t2 - t1, min_time)
            time_per_chunksize.append(min_time)
        min_time = 99999999
        # run a number of trials and pick the fastest to avoid jitter
        for trial in xrange(10):
            t1 = time.time()
            pool.map(check_prime, number_range)
            t2 = time.time()
            min_time = min(t2 - t1, min_time)
        mp_default_time = min_time
        mp_chunksize, mp_extra = divmod(len(number_range), NBR_PROCESSES * 4)
        if mp_extra:
            mp_chunksize += 1
        cPickle.dump((chunksizes, time_per_chunksize, mp_extra,
                      mp_chunksize, mp_default_time), open(filename, 'wb'))
    else:
        chunksizes, time_per_chunksize, mp_extra, mp_chunksize, mp_default_time = cPickle.load(
            open(filename))
        # make a figure, show the experimental timings
        f = plt.figure(1)
        plt.clf()
        plt.plot(chunksizes, time_per_chunksize, "bx-", label="experiments")
        ax = f.get_axes()[0]

        # annotate the timings
        for chunk_size, time_cost in zip(chunksizes, time_per_chunksize):
            ax.annotate('{:0.2f}s'.format(time_cost),
                        xy=(chunk_size, time_cost),
                        xytext=(5, 5),
                        ha='right',
                        textcoords='offset points',
                        fontsize='large')

        if plot_type == 1:
            plt.plot([mp_chunksize], [mp_default_time], "bo", label="default")
            plt.semilogx()  # convert x scale to log
        plt.ylabel("Completion time (seconds)")
        plt.xlabel("chunksize parameter")
        plt.legend(numpoints=1, framealpha=0.9)
        if plot_type == 1:
            plt.xlim(xmin=0.7)  # give a gap on the left edge
            plt.ylim(ymax=2.6)
        if plot_type == 2:
            plt.xlim(xmin=-0.5)
            plt.ylim(ymax=2.7)
        plt.title(
            "Time cost of varying chunksizes with {} processes for\nprime checking in range [{}-{}]".format(
                NBR_PROCESSES,
                min(number_range),
                max(number_range)))
        # plt.grid()
        # plt.show()
        # manually add plt.tight_layout()
        plt.tight_layout()
        plt.savefig(png_filename)
