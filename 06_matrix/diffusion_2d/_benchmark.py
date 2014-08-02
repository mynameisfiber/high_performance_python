#!/usr/bin/env python2.7

import diffusion_python
import diffusion_python_memory
import diffusion_numpy
import diffusion_numpy_memory
import diffusion_numpy_memory2
import diffusion_scipy
import diffusion_numpy_memory2_numexpr

from collections import defaultdict


def run_experiment(experiment, iterations, label, baseline=None):
    try:
        t = experiment.run_experiment(nruns)
        extra_runs = max(int(30 / t) - 1, 2)
        for i in xrange(extra_runs):
            test = experiment.run_experiment(nruns)
            t = min(t, test)
    except Exception as e:
        print "Could not run: %s: %s" % (label, e)
        raise

    speedup_label = ''
    if baseline:
        speedup_label = "[%0.2fx speedup]" % (baseline / t)
    _format = (label, t, t / float(nruns), speedup_label)
    print "%s: %0.2fs (%es per iteration)%s" % _format
    return t, (baseline or 0) / t


def set_grid_shape(grid_width):
    modules = (
        diffusion_python,
        diffusion_python_memory,
        diffusion_numpy,
        diffusion_numpy_memory,
        diffusion_scipy,
        diffusion_numpy_memory2,
        diffusion_numpy_memory2_numexpr)
    for m in modules:
        if m is not None:
            setattr(m, "grid_shape", (grid_width, grid_width))

if __name__ == "__main__":
    nruns = 50

    sizes = (256, 512, 1024, 2048, 4096)
    data = defaultdict(list)
    for grid_width in sizes:
        set_grid_shape(grid_width)
        print "Grid size: ", diffusion_python.grid_shape
        baseline, _ = run_experiment(diffusion_python, nruns, "Pure Python")
        data["python"].append((baseline, 0))
        data['python+memory'].append(
            run_experiment(
                diffusion_python_memory,
                nruns,
                "python+memory",
                baseline))
        data['numpy+memory'].append(
            run_experiment(
                diffusion_numpy_memory,
                nruns,
                "numpy+memory",
                baseline))
        data['numpy'].append(
            run_experiment(diffusion_numpy, nruns, "numpy", baseline))
        data['numpy+memory+laplace'].append(
            run_experiment(
                diffusion_numpy_memory2,
                nruns,
                "numpy+memory2",
                baseline))
        data['numpy+memory+laplace+numexpr'].append(
            run_experiment(
                diffusion_numpy_memory2_numexpr,
                nruns,
                "numpy+memory2+numexpr",
                baseline))
        data['numpy+memory+scipy'].append(
            run_experiment(
                diffusion_scipy,
                nruns,
                "numpy+memory+scipy",
                baseline))
        print ""

    print '[width="40%",frame="topbot",options="header"]\n|======================'
    print '|Method 2+|' + " 2+| ".join("%dx%d" % (s, s) for s in sizes) + '|'
    print '| |' + "|".join("runtime | speedup" for s in sizes) + '|'
    for method, data in data.iteritems():
        print "|" + method + "|" + "|".join('%0.2fs | %0.2fx' % d for d in data) + "|"
    print "|======================"
