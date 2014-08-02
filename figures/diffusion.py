#!/usr/bin/env python2.7

from numpy import (zeros, empty, multiply, copyto, asarray)
from numexpr import evaluate
import pylab as py
import urllib

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

if __name__ == "__main__":
    scratch_square = empty(grid_shape)
    grid_square = zeros(grid_shape)
    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid_square[block_low:block_high, block_low:block_high] = 0.005

    grid_python = 1 - py.imread(urllib.urlopen(
        "http://a4.mzstatic.com/us/r30/Purple4/v4/e8/20/fd/e820fded-8a78-06ac-79d0-f1d140346976/mzl.huoealqj.png")).mean(2)
    grid_python = asarray(grid_python, dtype='float64')
    scratch_python = empty(grid_python.shape)

    py.subplot(3, 2, 1)
    py.imshow(grid_square.copy())
    py.ylabel("t = 0 seconds")
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])
    py.subplot(3, 2, 2)
    py.imshow(grid_python.copy())
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])

    for i in range(500):
        evolve(grid_square, 0.1, scratch_square)
        grid_square, scratch_square = scratch_square, grid_square

        evolve(grid_python, 0.1, scratch_python)
        grid_python, scratch_python = scratch_python, grid_python

    py.subplot(3, 2, 3)
    py.imshow(grid_square.copy())
    py.ylabel("t = 50 seconds")
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])
    py.subplot(3, 2, 4)
    py.imshow(grid_python.copy())
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])

    for i in range(1000):
        evolve(grid_square, 0.2, scratch_square)
        grid_square, scratch_square = scratch_square, grid_square

        evolve(grid_python, 0.2, scratch_python)
        grid_python, scratch_python = scratch_python, grid_python

    py.subplot(3, 2, 5)
    py.imshow(grid_square.copy())
    py.ylabel("t = 250 seconds")
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])
    py.subplot(3, 2, 6)
    py.imshow(grid_python.copy())
    py.gca().get_xaxis().set_ticks([])
    py.gca().get_yaxis().set_ticks([])

    fig = py.gcf()
    fig.suptitle(r"Diffusion at $t=0s$, $t=50s$ and $t=250s$", fontsize=24)

    py.savefig("images/diffusion.png")
    py.show()
