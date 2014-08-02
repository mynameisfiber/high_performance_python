import math
import timeit


def check_prime(n):
    if n % 2 == 0:
        return False
    from_i = 3
    to_i = math.sqrt(n) + 1
    for i in xrange(from_i, int(to_i), 2):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    for label, nbr in [("trivial non-prime", 112272535095295),
                       ("expensive non-prime18_1", 100109100129100369),
                       ("expensive non-prime18_2", 100109100129101027),
                       # ("prime", 112272535095293)]:  # 15
                       #("prime17",  10000000002065383)]
                       ("prime18_1", 100109100129100151),
                       ("prime18_2", 100109100129162907)]:
                       #("prime23", 22360679774997896964091)]:

        time_costs = timeit.repeat(
            stmt="check_prime({})".format(nbr),
            repeat=20,
            number=1,
            setup="from __main__ import check_prime")
        print "{:24} ({}) {: 3.6f}s".format(label, nbr, min(time_costs))
