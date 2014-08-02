import math
import time
import multiprocessing
#import numpy as np
import itertools


def check_prime(n):
    if n % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    primes = []
    NBR_PROCESSES = 4
    pool = multiprocessing.Pool(processes=NBR_PROCESSES)

    t1 = time.time()
    # number_range = xrange(100000000, 100010000)  # A
    # number_range = xrange(100000000, 100100000)  # B
    number_range = xrange(100000000, 101000000)  # C
    # number_range = xrange(1000000000, 1000100000)  # D
    # number_range = xrange(100000000000, 100000100000)  # E

    # are_primes = pool.map(check_prime, number_range)  # original
    # primes = np.array(number_range)[np.array(are_primes)]  # original
    #
    # note using pool.map is fastest, but uses ram
    # using pool.imap is slower but uses less ram
    # pool.imap_unordered is even slower
    are_primes = pool.map(check_prime, number_range)
    primes = [p for p in itertools.compress(number_range, are_primes)]

    print "Took:", time.time() - t1
    print len(primes), primes[:10], primes[-10:]
