def calculate_z(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while n < maxiter and (z.real * z.real + z.imag * z.imag) < 4:
            z = z * z + c
            n += 1
        output[i] = n
    return output


if __name__ == "__main__":
    # make a trivial example using the correct types to enable type inference
    maxiter = 1
    zs = [complex(0, 0)]
    cs = [complex(-0.62772, -.42193)]
    # call the function so ShedSkin can analyze the types
    output = calculate_z(maxiter, zs, cs)
