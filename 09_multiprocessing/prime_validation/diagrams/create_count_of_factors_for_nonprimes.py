import argparse
import math
import multiprocessing
import cPickle
from collections import Counter
import matplotlib.pyplot as plt


def check_prime(n):
    if n % 100000 == 0:
        print n
    if n % 2 == 0:
        return False, 2
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False, i
    return True, None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument(
        '--create_data',
        action="store_true",
        default=False,
        help='if present then calculate data, if absent then plot')
    args = parser.parse_args()

    filename = "primes_validation_count_of_factors.pickle".format()
    png_filename = "primes_validation_count_of_factors.png".format()

    if args.create_data:
        upper_bound = 10000000
        number_range = xrange(3, upper_bound)
        NBR_PROCESSES = 4
        pool = multiprocessing.Pool(processes=NBR_PROCESSES)
        are_primes = pool.map(check_prime, number_range)
        c = Counter()
        for is_prime, factor in are_primes:
            if not is_prime:
                c.update([factor])
        # for n in number_range:
            #is_prime, factor = check_prime(n)
            # if not is_prime:
                # c.update([factor])
        PICKLED_DATA = (upper_bound, c)
        cPickle.dump(PICKLED_DATA, open(filename, 'wb'))
    else:
        (upper_bound, c) = cPickle.load(open(filename))
        #nbr_chunks_per_trial, time_per_chunksize, NBR_PROCESSES, number_range = cPickle.load(open(filename))
        # make a figure, show the experimental timings
        f = plt.figure(1)
        plt.clf()
        plt.barh(c.keys(), c.values(), log=True)
        #plt.plot(nbr_chunks_per_trial, time_per_chunksize, "bx-", label="experiments")
        #ax = f.get_axes()[0]
        plt.title(
            "Count of {:,} factors of non-primes to {:,}".format(len(c), upper_bound))
        plt.ylabel("Factor for non-prime")
        plt.xlabel("Frequency of factor")
        plt.ylim(ymax=max(c.keys()) + 100)
        plt.xlim(xmax=c[2] + 100)
        plt.tight_layout()
        plt.savefig(png_filename)
        # plt.show()
