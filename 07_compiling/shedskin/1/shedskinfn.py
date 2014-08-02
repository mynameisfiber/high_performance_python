def calculate_z(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)
    for i in range(len(zs)):
        n = 0
        z = zs[i]
        c = cs[i]
        while n < maxiter and abs(z) < 2:
            z = z * z + c
            n += 1
        output[i] = n
    return output


if __name__ == "__main__":
    # make a trivial example using the correct types to enable type inference
    # call the function so ShedSkin can analyze the types
    output = calculate_z(1, [0j], [0j])
