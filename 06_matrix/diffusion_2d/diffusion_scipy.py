#!/usr/bin/env python2.7

from numpy import (multiply, add, zeros)
from scipy.ndimage.filters import laplace
import time

grid_shape = (512, 512)


def laplacian(grid, out):
    laplace(grid, out, mode='wrap')


def evolve(grid, dt, out, D=1):
    laplacian(grid, out)
    multiply(out, D * dt, out)
    add(out, grid, grid)


def run_experiment(num_iterations):
    scratch = zeros(grid_shape)
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
