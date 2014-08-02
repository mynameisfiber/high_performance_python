#!/usr/bin/env python

import numpy as np
import pylab as py
import ctypes


def linear_probe(h, mask=0b111):
    while True:
        h = (5 * h + 1) & mask
        yield h


def modified_probe(h, mask=0b111, PERTURB_SHIFT=5):
    perturb = ctypes.c_size_t(h).value
    i = perturb & mask
    yield i
    while True:
        i = (i << 2) + i + perturb + 1
        perturb >>= PERTURB_SHIFT
        yield i & mask


def cover_space(iterable, digits):
    s = set()
    for i, v in enumerate(iterable):
        yield i, v
        if v not in s:
            s.add(v)
            if len(s) == digits:
                return


def table():
    dict_length = 8
    data = {"linear": {}, "pert": {}}
    for h in (0b100, 0b110101001011100):
        indexes = linear_probe(h, dict_length - 1)
        data["linear"][h] = [v for i, v in cover_space(indexes, dict_length)]

        indexes = modified_probe(h, dict_length - 1)
        data["pert"][h] = [v for i, v in cover_space(indexes, dict_length)]

    print data


def plot():
    dict_length = 1 << 3
    key = 2500

    indexes = modified_probe(hash(key), dict_length - 1)
    index_values = list(cover_space(indexes, dict_length))

    print "--"
    color_data = np.zeros((dict_length, 1)) - 1
    for i, v in index_values:
        if color_data[v, 0] == -1:
            print i, v
            color_data[v, 0] = i
    print color_data.T
    py.imshow(color_data.T, interpolation='None', aspect='auto')

    axis = py.gca()
    axis.axes.get_xaxis().set_ticks([])
    axis.axes.get_yaxis().set_ticks([])
    py.xlabel("Index for underlying dictionary data")

    for i, d in index_values:
        y = -0.4 * (1 - i * 2.0 / len(index_values))
        py.text(d - 0.25, y, "%2d" % int(i), color="white", fontsize=15)
        py.text(d - 0.25, y, "%2d" % int(i), color="black", fontsize=13)

    py.colorbar(orientation='horizontal')
    py.savefig("images/dict_probing.png")
    py.show()

if __name__ == "__main__":
    table()
    plot()
