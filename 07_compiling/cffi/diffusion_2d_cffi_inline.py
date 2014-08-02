#!/usr/bin/env python2.7

import numpy as np
import time
from cffi import FFI, verifier

grid_shape = (512, 512)

ffi = FFI()
ffi.cdef(
    r'''void evolve(int Nx, int Ny, double **in, double **out, double D, double dt);''')
lib = ffi.verify(r'''
void evolve(int Nx, int Ny, double in[][Ny], double out[][Ny], double D, double dt) {
    int i, j;
    double laplacian;
    for (i=1; i<Nx-1; i++) {
        for (j=1; j<Ny-1; j++) {
            laplacian = in[i+1][j] + in[i-1][j] + in[i][j+1] + in[i][j-1] - 4 * in[i][j];
            out[i][j] = in[i][j] + D * dt * laplacian;
        }
    }
}
''', extra_compile_args=["-O3", ])


def evolve(grid, dt, out, D=1.0):
    X, Y = grid_shape
    pointer_grid = ffi.cast('double**', grid.ctypes.data)
    pointer_out = ffi.cast('double**', out.ctypes.data)
    lib.evolve(X, Y, pointer_grid, pointer_out, D, dt)


def run_experiment(num_iterations):
    scratch = np.zeros(grid_shape, dtype=np.double)
    grid = np.zeros(grid_shape, dtype=np.double)

    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, 0.1, scratch)
        grid, scratch = scratch, grid
    return time.time() - start

if __name__ == "__main__":
    t = run_experiment(500)
    print t

    verifier.cleanup_tmpdir()
