import timeit


def search_fast(haystack, needle):
    for item in haystack:
        if item == needle:
            return True
    return False


def search_slow(haystack, needle):
    return_value = False
    for item in haystack:
        if item == needle:
            return_value = True
    return return_value


if __name__ == "__main__":
    setup = 'from __main__ import (haystack, needle, search_fast, search_slow)'
    iterations = 10000
    haystack = range(1000)

    needle = 5
    print "Testing search speed with {} items and needle " \
        "close to the head of the list".format(len(haystack))

    t = timeit.timeit(
        stmt='search_fast(haystack, needle)',
        setup=setup,
        number=iterations
    )
    print "search_fast time: {:.5e}".format(t / float(iterations))

    t = timeit.timeit(
        stmt='search_slow(haystack, needle)',
        setup=setup,
        number=iterations
    )
    print "search_slow time: {:.5e}".format(t / float(iterations))

    needle = len(haystack) - 10
    print "Testing search speed with {} items and needle " \
        "close to the tail of the list".format(len(haystack))

    t = timeit.timeit(
        stmt='search_fast(haystack, needle)',
        setup=setup,
        number=iterations
    )
    print "search_fast time: {:.5e}".format(t / float(iterations))

    t = timeit.timeit(
        stmt='search_slow(haystack, needle)',
        setup=setup,
        number=iterations
    )
    print "search_slow time: {:.5e}".format(t / float(iterations))
