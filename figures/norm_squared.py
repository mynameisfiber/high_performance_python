#!/usr/bin/env python2.7

import sys
import os
sys.path.append(os.path.abspath("../06_matrix/norm/"))

import norm_array
import norm_numpy
import norm_numpy_dot
import norm_python
import norm_python_comprehension

from itertools import cycle

import numpy as np
import pylab as py

methods = {k: v for k, v in globals().iteritems() if k.startswith("norm")}
markers = cycle('h*o>Dxsp8')
linestyles = cycle(['-', ':', '--', '-.'])

if __name__ == "__main__":
    timings = {k: [] for k in methods}
    for exponent in xrange(12, 40):
        N = int(1.5 ** exponent)
        print "exponent:", exponent
        print "N:", N
        for name, method in methods.iteritems():
            t = method.run_experiment(N, num_iter=5) * 1000.0
            timings[name].append((N, t))
            print "%s: %f" % (name, t)

    for name, data in timings.iteritems():
        d = np.asarray(data)
        py.plot(d[:, 0], d[:, 1], label=name, marker=markers.next(),
                linestyle=linestyles.next(), linewidth=4)

    py.title("Runtime for various norm squared routines")
    py.xlabel("Vector length")
    py.ylabel("Runtime (miliseconds) -- less is better")
    py.legend(loc='upper left', handlelength=5)

    py.tight_layout()
    py.savefig("images/norm_squared.png")
    py.show()
