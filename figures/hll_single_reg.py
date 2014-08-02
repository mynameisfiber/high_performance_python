#!/usr/bin/env python

import numpy as np
import pylab as py
import countmemaybe


def leading_set_bit(number):
    number_binary = bin(number)
    return len(number_binary) - number_binary.rfind('1')


class HLL(object):
    max_index = 0

    def add(self, number):
        index = leading_set_bit(number)
        self.max_index = max(self.max_index, index)

    def __len__(self):
        return 2 ** self.max_index

if __name__ == "__main__":
    data_list = []
    h1 = HLL()
    h = countmemaybe.HyperLogLog()
    for i in xrange(100000):
        item = "seee%seeeed234rsdaf" % i
        x = h._hash(item)
        h1.add(x)
        h.add(x)
        data_list.append((i + 1, len(h1), len(h)))

    data_numpy = np.asarray(data_list)
    py.plot(data_numpy[:, 0], data_numpy[:, 1],
            ':', label="Single HLL Register")
    py.plot(data_numpy[:, 0], data_numpy[:, 2],
            '--', label="HLL with 16 registers")
    py.plot(data_numpy[:, 0], data_numpy[:, 0], label="Actual Size")
    py.legend(loc='upper left')

    py.title("Performance of a single HLL Register")
    py.xlabel("Size of the set")
    py.ylabel("Predicted size of the set")

    py.savefig("images/hll_single_reg.png")
    py.show()
