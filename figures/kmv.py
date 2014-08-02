#!/usr/bin/env python

import sys
import os
sys.path.append(
    os.path.abspath("../11_less_ram/probabilistic_datastructures/"))

from kminvalues import KMinValues
import pylab as py


def plot(kmv):
    py.scatter([d / float(2 ** 32 - 1)
                for d in kmv.data[:-1]], [0] * (len(kmv.data) - 1), alpha=0.25)
    py.axvline(x=(kmv.data[-2] / float(2 ** 32 - 1)), c='r')
    py.gca().get_yaxis().set_visible(False)
    py.gca().get_xaxis().set_ticklabels([])
    py.gca().get_xaxis().set_ticks([x / 10. for x in xrange(11)])

if __name__ == "__main__":
    k = 20
    num_panels = 20
    kmv = KMinValues(k)
    for i in xrange(k * num_panels + 1):
        if i % k == 0 and i != 0:
            py.subplot(num_panels, 1, i // k)
            if i == k:
                py.title("Hash space density for KMV with k=%d" % k)
            plot(kmv)
            py.xlim((0, 1))
        kmv.add(str(i))

    py.gca().get_xaxis().set_ticks([x / 10. for x in xrange(11)])
    py.gca().get_xaxis().set_ticklabels([x / 10. for x in xrange(11)])

    py.tight_layout()
    py.savefig("images/kmv.png")
    py.show()
