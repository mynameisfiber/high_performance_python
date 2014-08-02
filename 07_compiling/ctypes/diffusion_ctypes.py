import numpy as np
import time
import ctypes

grid_shape = (512, 512)
_diffusion = ctypes.CDLL("../diffusion.so")

# Create references to the C types that we will need to simplify future code
TYPE_INT = ctypes.c_int
TYPE_DOUBLE = ctypes.c_double
TYPE_DOUBLE_SS = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

# Initialize the signature of the evolve function to:
# void evolve(int, int, double**, double**, double, double)
_diffusion.evolve.argtypes = [
    TYPE_INT,
    TYPE_INT,
    TYPE_DOUBLE_SS,
    TYPE_DOUBLE_SS,
    TYPE_DOUBLE,
    TYPE_DOUBLE,
]
_diffusion.evolve.restype = None


def evolve(grid, out, dt, D=1.0):
    # First we convert the python types into the relevant C types
    cX = TYPE_INT(grid_shape[0])
    cY = TYPE_INT(grid_shape[1])
    cdt = TYPE_DOUBLE(dt)
    cD = TYPE_DOUBLE(D)
    pointer_grid = grid.ctypes.data_as(TYPE_DOUBLE_SS)
    pointer_out = out.ctypes.data_as(TYPE_DOUBLE_SS)

    # Now we can call the function
    _diffusion.evolve(cX, cY, pointer_grid, pointer_out, cD, cdt)


def run_experiment(num_iterations):
    scratch = np.zeros(grid_shape, dtype=ctypes.c_double)
    grid = np.zeros(grid_shape, dtype=ctypes.c_double)

    block_low = int(grid_shape[0] * .4)
    block_high = int(grid_shape[0] * .5)
    grid[block_low:block_high, block_low:block_high] = 0.005

    start = time.time()
    for i in range(num_iterations):
        evolve(grid, scratch, 0.1)
        grid, scratch = scratch, grid
    return time.time() - start

if __name__ == "__main__":
    t = run_experiment(500)
    print t
