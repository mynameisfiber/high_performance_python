import time
import ctypes
from contextlib import contextmanager
from progressbar import ProgressBar, ETA, Bar, Percentage

import cPickle
from pprint import pprint

from morriscounter import MorrisCounter
from llregister import LLRegister
from ll import LL
from superll import SuperLL
from countmemaybe import HyperLogLog, KMinValues
from scalingbloomfilter import ScalingBloomFilter

methods = [
    {
        "name": "Morris Counter",
        "obj": MorrisCounter(),
    },
    {
        "name": "Log Log Register",
        "obj": LLRegister(),
    },
    {
        "name": "LogLog",
        "obj": LL(16),
    },
    {
        "name": "SuperLogLog",
        "obj": SuperLL(16),
    },
    {
        "name": "HyperLogLog",
        "obj": HyperLogLog(b=16),
    },
    {
        "name": "KMinValues",
        "obj": KMinValues(k=1 << 16),
    },
    {
        "name": "ScalingBloom",
        "obj": ScalingBloomFilter(1048576),
    },
]


@contextmanager
def TimerBlock(name):
    start = time.time()
    t = ctypes.c_double()
    try:
        yield t
    finally:
        t.value = time.time() - start
        print "[%s] took %s seconds" % (name, t.value)


def wikireader(filename, buffering=1 << 10):
    maxval = 1148708949
    with open(filename, 'r', buffering=buffering) as fd:
        p = ProgressBar(
            maxval=maxval, widgets=[Percentage(), Bar(), ETA()]).start()
        for line in p(fd):
            yield line.strip()

if __name__ == "__main__":
    filename = "/export/bbq1/micha/wiki_data/enwiki-latest-pages-articles.tokens"

    print "baseline reading measurement"
    with TimerBlock("Iterate File") as baseline:
        tmp = 0
        for line in wikireader(filename):
            tmp += len(line)

    for method in methods:
        print method['name']
        obj = method['obj']
        with TimerBlock("Iterate File") as bench:
            for line in wikireader(filename):
                obj.add(line)
        method['time'] = bench.value - baseline.value
        method['estimate'] = len(obj)

    pprint(methods)
    cPickle.dump(methods, open("_benchmark.pkl", "w+"))
