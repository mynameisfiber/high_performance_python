#!/usr/bin/env python2.7

from numpy import (copyto, multiply, zeros)
from numexpr import (evaluate, set_num_threads)
import time

grid_shape = (512, 512)


def roll_add(rollee, shift, axis, out):
    if shift == 1 and axis == 0:
        out[1:, :] += rollee[:-1,:]
        out[0, :] += rollee[-1,:]
    elif shift == -1 and axis == 0:
        out[:-1, :] += rollee[1:,:]
        out[-1, :] += rollee[0,:]
    elif shift == 1 and axis == 1:
        out[:, 1:] += rollee[:, :-1]
        out[:, 0] += rollee[:, -1]
    elif shift == -1 and axis == 1:
        out[:, :-1] += rollee[:, 1:]
        out[:, -1] += rollee[:, 0]


def laplacian(grid, out):
    copyto(out, grid)
    multiply(out, -4.0, out)
    roll_add(grid, +1, 0, out)
    roll_add(grid, -1, 0, out)
    roll_add(grid, +1, 1, out)
    roll_add(grid, -1, 1, out)


def evolve(grid, dt, out, D=1):
    laplacian(grid, out)
    evaluate("out*D*dt+grid", out=out)


def run_experiment(num_iterations):
    previous_threads = set_num_threads(1)

    scratch = zeros(grid_shape)
    grid = zeros(grid_shape)

    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid

    set_num_threads(previous_threads)
    return time.time() - start

if __name__ == "__main__":
    run_experiment(500)
