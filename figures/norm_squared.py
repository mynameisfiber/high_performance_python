#!/usr/bin/env python2.7

import sys
import os
sys.path.append(os.path.abspath("../06_matrix/norm/"))

import norm_array
import norm_numpy
import norm_numpy_dot
import norm_python
import norm_python_comprehension
import norm_python_generator

from itertools import cycle

import numpy as np
import pylab as py

plot_name = {
    "norm_array" : "norm_square_array",
    "norm_numpy" : "norm_square_numpy",
    "norm_numpy_dot" : "norm_square_numpy_dot",
    "norm_python" : "norm_square_list",
    "norm_python_comprehension": "norm_square_list_comprehension",
    "norm_python_generator" : "norm_square_generator_comprehension",
}

methods = {plot_name[k]:v for k,v in globals().iteritems() if k.startswith("norm")}
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

    timings = list(timings.iteritems())
    timings.sort(key = lambda (k, v) : np.mean([i[1] for i in v]), reverse=True)
    for name, data in timings:
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
