"""Julia set generator without optional PIL-based image drawing"""
import numba
from numba import jit
import time
import numpy as np

# area of complex space to investigate
x1, x2, y1, y2 = -1.8, 1.8, -1.8, 1.8
c_real, c_imag = -0.62772, -.42193

# type output
#('output has type:', array(int32, 1d, C))
#('zs has type:', array(complex128, 1d, C))
# cs has type: array(complex128, 1d, C)
# output has type: array(int32, 1d, C)


@jit()  # (nopython=True)
def calculate_z_serial_purepython(maxiter, zs, cs, output):
    """Calculate output list using Julia update rule"""
    #output = numba.numpy_support.numpy.zeros(len(zs), dtype=np.int32)
    #print("output has type:", numba.typeof(output))
    #print("zs has type:", numba.typeof(zs))
    #print("cs has type:", numba.typeof(cs))
    #print("output has type:", numba.typeof(output))
    for i in xrange(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        # while n < maxiter and abs(z) < 2:
        while n < maxiter and z.real * z.real + z.imag * z.imag < 4:
            z = z * z + c
            n += 1
        output[i] = n
    # return output


#@profile
def calc_pure_python(draw_output, desired_width, max_iterations):
    """Create a list of complex co-ordinates (zs) and complex parameters (cs), build Julia set and display"""
    x_step = (float(x2 - x1) / float(desired_width))
    y_step = (float(y1 - y2) / float(desired_width))
    x = []
    y = []
    ycoord = y2
    while ycoord > y1:
        y.append(ycoord)
        ycoord += y_step
    xcoord = x1
    while xcoord < x2:
        x.append(xcoord)
        xcoord += x_step
    # build a list of co-ordinates and the initial condition for each cell.
    # Note that our initial condition is a constant and could easily be removed,
    # we use it to simulate a real-world scenario with several inputs to our
    # function
    zs = []
    cs = []
    for ycoord in y:
        for xcoord in x:
            zs.append(complex(xcoord, ycoord))
            cs.append(complex(c_real, c_imag))

    print("Length of x:", len(x))
    print("Total elements:", len(zs))
    zs2 = np.array(zs, np.complex128)
    cs2 = np.array(cs, np.complex128)
    start_time = time.time()
    output = np.zeros_like(zs2, dtype=np.int32)
    calculate_z_serial_purepython(max_iterations, zs2, cs2, output)
    end_time = time.time()
    secs = end_time - start_time
    print("took", secs, "seconds")

    validation_sum = sum(output)
    print("Total sum of elements (for validation):", validation_sum)


# Calculate the Julia set using a pure Python solution with
# reasonable defaults for a laptop
# set draw_output to True to use PIL to draw an image
calc_pure_python(draw_output=False, desired_width=1000, max_iterations=300)
