import math
import time
import cPickle
import argparse
import matplotlib.pyplot as plt
import numpy as np


def check_prime(N):
    sqrtN = math.sqrt(N)
    Nf = float(N)
    for i in xrange(2, int(sqrtN) + 1):
        if (Nf / i).is_integer():
            return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument(
        '--create_data',
        action="store_true",
        default=False,
        help='if present then calculate data, if absent then plot')
    args = parser.parse_args()
    filename = "08_prime_time_cost_1e4to1e6.pickle"

    if args.create_data:
        primes = []
        are_primes = []
        times = []
        # explanation
        #lower_range = 3
        #upper_range = 1000
        # good range
        lower_range = 10001
        upper_range = 1000000
        numbers_to_test = np.array(range(lower_range, upper_range, 10))
        for possible_prime in numbers_to_test:
            min_time = 9999
            # calculate several times so we record the fastest time
            for loop in xrange(20):
                t1 = time.time()
                is_prime = check_prime(possible_prime)
                t2 = time.time()
                min_time = min(t2 - t1, min_time)
            times.append(min_time)
            # we only need to apped the result once
            if is_prime:
                primes.append(possible_prime)
            are_primes.append(is_prime)
        print primes[:10], primes[-10:]
        are_primes = np.array(are_primes)
        times = np.array(times)
        cPickle.dump(
            (numbers_to_test, are_primes, times), open(filename, 'wb'))
    else:
        numbers_to_test, are_primes, times = cPickle.load(open(filename))
        # plot the two items three times, the last doesn't have a label (but is
        # there to over-plot the Not Prime result), so the Legend items are
        # displayed in the correct sequence
        plt.plot(numbers_to_test[are_primes], times[
                 are_primes], 'x', color='k', alpha=1, label="Prime")
        plt.plot(
            numbers_to_test[
                are_primes == False],
            times[
                are_primes == False],
            '.',
            color='b',
            alpha=0.6,
            label="Not prime")
        plt.plot(numbers_to_test[are_primes], times[
                 are_primes], 'x', color='k', alpha=1, )
        plt.xlabel("Integers to test")
        plt.ylabel("Seconds per test")
        plt.title("Time cost for checking primality")
        plt.ylim(0, 0.00015)  # fits neatly on Ian's laptop
        # plt.grid()
        plt.legend()
        plt.savefig("08_prime_time_cost_1e4to1e6.png")
        plt.tight_layout()
        # plt.show()
