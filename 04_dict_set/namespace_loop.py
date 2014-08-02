from math import sin


def tight_loop_slow(iterations):
    """
    >>> %timeit tight_loop_slow(10000000)
    1 loops, best of 3: 2.21 s per loop
    """
    result = 0
    for i in xrange(iterations):
        # this call to sin requires a global lookup
        result += sin(i)


def tight_loop_fast(iterations):
    """
    >>> %timeit tight_loop_fast(10000000)
    1 loops, best of 3: 2.02 s per loop
    """
    result = 0
    local_sin = sin
    for i in xrange(iterations):
        # this call to local_sin requires a local lookup
        result += local_sin(i)
