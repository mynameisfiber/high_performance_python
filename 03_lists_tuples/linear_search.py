import timeit


def linear_search(needle, haystack):
    for i, item in enumerate(haystack):
        if item == needle:
            return i
    return -1


if __name__ == "__main__":
    setup = "from __main__ import (linear_search, haystack, needle)"
    iterations = 1000

    for haystack_size in (10000, 100000, 1000000):
        haystack = range(haystack_size)
        for needle in (1, 6000, 9000, 1000000):
            index = linear_search(needle, haystack)
            t = timeit.timeit(
                stmt='linear_search(needle, haystack)',
                setup=setup,
                number=iterations
            )
            print "Value {: <8} found in haystack of size {: <8} at index " \
                "{: <8} in {:.5e} seconds".format(
                    needle,
                    len(haystack),
                    index,
                    t / iterations
                )
