#!/usr/bin/env python

import sys
import os
sys.path.append(
    os.path.abspath("../11_less_ram/probabilistic_datastructures/"))

from morriscounter import MorrisCounter
from llregister import LLRegister
from scalingbloomfilter import ScalingBloomFilter
from hyperloglog import HyperLogLog
from kminvalues import KMinValues

from random import sample
import string

from itertools import cycle

import pylab as py
import numpy as np


def generate_keys(num_keys, num_letters):
    for i in xrange(num_keys):
        yield "".join(sample(string.ascii_lowercase, num_letters))


methods = [
    {
        "name": "Exact Solution",
        "init": set,
    },
    {
        "name": "Morris Counter",
        "init": MorrisCounter,
    },
    {
        "name": "Log Log Register",
        "init": LLRegister,
    },
    #{
    #"name" : "LogLog",
    #"init" : lambda : LL(4),
    #},
    #{
    #"name" : "SuperLogLog",
    #"init" : lambda : SuperLL(4),
    #},
    {
        "name": "HyperLogLog",
        "init": lambda: HyperLogLog(4),
    },
    {
        "name": "KMinValues",
        "init": lambda: KMinValues(2 << 4),
    },
    {
        "name": "ScalingBloom",
        "init": lambda: ScalingBloomFilter(2048),
    },
]


def run_experiment(exp_name, filename, key_generator, data, sample_freq=3000):
    for item in data:
        item["_tmp"] = item["init"]()
        item[exp_name] = []

    for i, key in enumerate(key_generator):
        for item in data:
            item["_tmp"].add(str(key))
            if i % sample_freq == 0:
                item[exp_name].append((i, len(item["_tmp"])))

    print "%s summary:" % exp_name
    for item in data:
        print "\t%-24s: %d" % (item["name"], len(item["_tmp"]))
        item.pop("_tmp")

    py.figure()
    plot_experiment(exp_name, data, filename)


def plot_experiment(exp_name, data, filename):
    markers = cycle('h*o>Dxsp8')
    py.title(exp_name)
    ymax = []
    for item in data:
        name = item["name"]
        data_ndarray = np.asarray(item[exp_name])
        ymax.append(data_ndarray[-1][1])
        py.plot(data_ndarray[:, 0], data_ndarray[:, 1], label=name,
                marker=markers.next(), alpha=0.6, markersize=8)
    py.legend(loc="best", fontsize='medium')
    py.xlabel("Items Added")
    py.ylabel("Size of set")

    ymax.sort()
    py.ylim(ymax=ymax[-2] * 1.1)
    py.savefig("images/prod_ds_%s.png" % filename)


if __name__ == "__main__":
    run_experiment("Unique Items", "unique", xrange(100000), methods)
    run_experiment(
        "60000 elements with duplicates",
        "dup",
        generate_keys(
            60000,
            3),
        methods)
    py.show()
