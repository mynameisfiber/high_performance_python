import math
import time


def check_prime(n):
    if n % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    primes = []
    t1 = time.time()
    # number_range = xrange(100000000, 100010000)  # A
    # number_range = xrange(100000000, 100100000)  # B
    number_range = xrange(100000000, 101000000)  # C
    # number_range = xrange(1000000000, 1000100000)  # D
    # number_range = xrange(100000000000, 100000100000)  # E

    for possible_prime in number_range:
        if check_prime(possible_prime):
            primes.append(possible_prime)

    print "Took:", time.time() - t1
    print len(primes), primes[:10], primes[-10:]
