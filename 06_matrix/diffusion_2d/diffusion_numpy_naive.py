#!/usr/bin/env python2.7

from numpy import (roll, zeros)
import time

grid_shape = (512, 512)


def laplacian(grid):
    return roll(grid, +1, 0) + roll(grid, -1, 0) + \
        roll(grid, +1, 1) + roll(grid, -1, 1) - 4 * grid


def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)


def run_experiment(num_iterations):
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
