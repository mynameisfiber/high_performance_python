#!/usr/bin/env python2.7

import numpy as np
import pylab as py

grid_size = (512, )


def laplacian(grid):
    return np.roll(grid, +1) + np.roll(grid, -1) - 2 * grid


def evolve(grid, dt, D=1):
    return grid + dt * D * laplacian(grid)

if __name__ == "__main__":
    grid = np.zeros(grid_size)
    max_val = 1.0

    block_low = int(grid_size[0] * .4)
    block_high = int(grid_size[0] * .6)
    grid[block_low:block_high] = max_val

    t = 0
    grids = [(t, grid.copy()), ]
    for i in xrange(3):
        for i in range(5000 * (4 ** i) + 1):
            grid = evolve(grid, 0.1)
        t += i * 0.1
        grids.append((t, grid.copy()))

    py.figure()
    for i, (t, grid) in enumerate(grids):
        py.subplot(len(grids), 1, i + 1)
        py.plot(grid)
        py.ylabel("t = %0.0f" % t)
        py.ylim(ymin=0, ymax=max_val * 1.1)
        py.xlim(xmin=0, xmax=grid_size[0])

    py.xlabel("Position")

    py.subplot(len(grids), 1, 1)
    py.title("1D Diffusion of a square function")

    py.tight_layout()
    py.savefig("images/diffusion_1d.png")
    py.show()
