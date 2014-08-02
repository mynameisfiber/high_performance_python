#!/usr/bin/env python2.7

from __future__ import division
import time

grid_size = (512, )


def laplacian(grid):
    lap = [0.0, ] * grid_size[0]
    xmax, = grid_size
    for i in xrange(grid_size[0]):
        grid_xx = grid[(i + 1) % xmax] + grid[(i - 1) % xmax] - 2.0 * grid[i]
        lap[i] = grid_xx
    return lap


def evolve(grid, dt, D=1.0):
    lap = laplacian(grid)
    for i in xrange(grid_size[0]):
        grid[i] += D * lap[i] * dt
    return grid


def run_experiment(num_iterations):
    # setting up initial conditions
    grid = [0.0, ] * grid_size[0]

    block_low = int(grid_size[0] * .4)
    block_high = int(grid_size[0] * .5)
    for i in xrange(block_low, block_high):
        grid[i] = 0.005

    start = time.time()
    for i in range(num_iterations):
        grid = evolve(grid, 0.1)
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
