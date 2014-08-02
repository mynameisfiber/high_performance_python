#!/usr/bin/env python2.7

import numpy as np
import time

grid_size = (512,)


def laplacian(grid, out):
    np.copyto(out, grid)
    np.multiply(out, -2.0, out)
    np.add(out, np.roll(grid, +1), out)
    np.add(out, np.roll(grid, -1), out)


def evolve(grid, dt, out, D=1):
    laplacian(grid, out)
    np.multiply(out, D * dt, out)
    np.add(out, grid, out)


def run_experiment(num_iterations):
    scratch = np.zeros(grid_size)
    grid = np.zeros(grid_size)

    block_low = int(grid_size[0] * .4)
    block_high = int(grid_size[0] * .5)
    grid[block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
