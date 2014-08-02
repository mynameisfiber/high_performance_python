#!/usr/bin/env python2.7

import numpy as np
import time

grid_size = (512, )


def laplacian(grid):
    return np.roll(grid, +1) + np.roll(grid, -1) - 2 * grid


def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)


def run_experiment(num_iterations):
    grid = np.zeros(grid_size)

    block_low = int(grid_size[0] * .4)
    block_high = int(grid_size[0] * .5)
    grid[block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
