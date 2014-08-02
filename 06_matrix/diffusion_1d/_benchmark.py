#!/usr/bin/env python2.7

import diffusion_python
import diffusion_python_memory
import diffusion_numpy
import diffusion_numpy_memory
import diffusion_numpy_memory2
import diffusion_scipy
import diffusion_numpy_memory2_numexpr


def run_experiment(experiment, iterations, label, baseline=None):
    try:
        t = experiment.run_experiment(nruns)
    except Exception as e:
        print "Could not run: %s: %s" % (label, e)
        raise

    speedup_label = ''
    if baseline:
        speedup_label = "[%0.2fx speedup]" % (baseline / t)
    _format = (label, t, t / float(nruns), speedup_label)
    print "%s: %0.2fs (%es per iteration)%s" % _format
    return t


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
            setattr(m, "grid_shape", (grid_width,))

if __name__ == "__main__":
    nruns = 50

    for grid_width in (1024, 2048, 8192):
        set_grid_shape(grid_width)
        print "Grid size: ", diffusion_python.grid_shape
        baseline = run_experiment(diffusion_python, nruns, "Pure Python")
        run_experiment(
            diffusion_python_memory, nruns, "python+memory", baseline)
        run_experiment(diffusion_numpy_memory, nruns, "numpy+memory", baseline)
        run_experiment(diffusion_numpy, nruns, "numpy", baseline)
        run_experiment(
            diffusion_numpy_memory2, nruns, "numpy+memory2", baseline)
        run_experiment(
            diffusion_numpy_memory2_numexpr,
            nruns,
            "numpy+memory2+numexpr",
            baseline)
        run_experiment(diffusion_scipy, nruns, "numpy+memory+scipy", baseline)
        print ""
