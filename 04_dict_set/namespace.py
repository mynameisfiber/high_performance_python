import math
from math import sin


def test1(x):
    """
    >>> %timeit test1(123456)
    1000000 loops, best of 3: 381 ns per loop
    """
    return math.sin(x)


def test2(x):
    """
    >>> %timeit test2(123456)
    1000000 loops, best of 3: 311 ns per loop
    """
    return sin(x)


def test3(x, sin=math.sin):
    """
    >>> %timeit test3(123456)
    1000000 loops, best of 3: 306 ns per loop
    """
    return sin(x)
