#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Approximate Morris Counter supporting many counters"""
from __future__ import division  # 1/2 == 0.5, as in Py3
# avoid hiding global modules with locals
from __future__ import absolute_import
from __future__ import print_function  # force use of print("hello")
# force unadorned strings "" to be unicode without prepending u""
from __future__ import unicode_literals
import math
import random
import array

SMALLEST_UNSIGNED_INTEGER = b'B'  # typically 1 byte on 64 bit systems
# b'I' unsigned integer 4 bytes on 64 bit systems
# b'L' unsigned integer 8 bytes on 64 bit systems


class MorrisCounter(object):

    """Approximate counter, stores exponent and counts approximately 2^exponent

    https://en.wikipedia.org/wiki/Approximate_counting_algorithm"""

    def __init__(self, type_code=SMALLEST_UNSIGNED_INTEGER, nbr_counters=1):
        self.exponents = array.array(type_code, [0] * nbr_counters)

    def __len__(self):
        return len(self.exponents)

    def add_counter(self):
        """Add a new zeroed counter"""
        self.exponents.append(0)

    def get(self, counter=0):
        """Calculate approximate value represented by counter"""
        return math.pow(2, self.exponents[counter])

    def add(self, counter=0):
        """Probabilistically add 1 to counter"""
        value = self.get(counter)
        probability = 1.0 / value
        if random.uniform(0, 1) < probability:
            self.exponents[counter] += 1

if __name__ == "__main__":
    mc = MorrisCounter()
    print("MorrisCounter has {} counters".format(len(mc)))
    for n in range(10):
        print("Iteration %d, MorrisCounter has: %d" % (n, mc.get()))
        mc.add()

    for n in xrange(990):
        mc.add()
    print("Iteration 1000, MorrisCounter has: %d" % (mc.get()))
