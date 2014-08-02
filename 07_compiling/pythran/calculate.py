import numpy as np

# pythran export calculate_z(int, complex[], complex[], int[])


def calculate_z(maxiter, zs, cs, output):
    """Calculate output list using Julia update rule"""
    # omp parallel for schedule(guided)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        # while n < maxiter and abs(z) < 2:
        while n < maxiter and (z.real * z.real + z.imag * z.imag) < 4:
            z = z * z + c
            n += 1
        output[i] = n
    return output
