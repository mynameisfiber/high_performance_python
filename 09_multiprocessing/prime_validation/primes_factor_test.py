import math
import time


def check_prime(n):
    if n % 2 == 0:
        return False, 2
    for i in xrange(3, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False, i
    return True, None


if __name__ == "__main__":
    primes = []
    t1 = time.time()

    #  100109100129100151 big prime
    # http://primes.utm.edu/curios/page.php/100109100129100151.html
    #number_range = xrange(100109100129100153, 100109100129101238, 2)
    number_range = xrange(100109100129101237, 100109100129201238, 2)

    # new expensive near-primes
    # [(95362951, (100109100129100369, 7.254560947418213))
    # (171656941, (100109100129101027, 13.052711009979248))
    # (121344023, (100109100129101291, 8.994053840637207)
    # note these two lines of timings look really wrong, they're about 4sec
    # each really
    # [(265687139, (100109100129102047, 19.642582178115845)), (219609683, (100109100129102277, 16.178056001663208)), (121344023, (100109100129101291, 8.994053840637207))]
    # [(316096873, (100109100129126653, 23.480671882629395)), (313994287, (100109100129111617, 23.262380123138428)), (307151363, (100109100129140177, 22.80288815498352))]
    # primes
    # 100109100129162907
    # 100109100129162947

    highest_factors = {}
    for possible_prime in number_range:
        t2 = time.time()
        is_prime, factor = check_prime(possible_prime)
        if is_prime:
            primes.append(possible_prime)
            print "GOT NEW PRIME", possible_prime
        else:
            highest_factors[factor] = (possible_prime, time.time() - t2)
            hf = highest_factors.items()
            hf.sort(reverse=True)
            print hf[:3]
    print "Took:", time.time() - t1
    print len(primes), primes[:10], primes[-10:]
