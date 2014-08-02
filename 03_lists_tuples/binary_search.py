import timeit


def binary_search(needle, haystack):
    # imin and imax store the bounds of the haystack that we are currently
    # considering.  This starts as the bounds of the haystack and slowly
    # converges to surround the needle.
    imin, imax = 0, len(haystack)
    while True:
        if imin >= imax:
            return -1
        midpoint = (imin + imax) // 2
        if haystack[midpoint] > needle:
            imax = midpoint
        elif haystack[midpoint] < needle:
            imin = midpoint + 1
        else:
            return midpoint


if __name__ == "__main__":
    setup = "from __main__ import (binary_search, haystack, needle)"
    iterations = 10000

    for haystack_size in (10000, 100000, 1000000):
        haystack = range(haystack_size)
        for needle in (1, 6000, 9000, 1000000):
            index = binary_search(needle, haystack)
            t = timeit.timeit(
                stmt='binary_search(needle, haystack)',
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
