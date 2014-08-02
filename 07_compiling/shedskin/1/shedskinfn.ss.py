# maxiter: [int], zs: [list(complex)], cs: [list(complex)]
def calculate_z(maxiter, zs, cs):
    """Calculate output list using Julia update rule"""
    output = [0] * len(zs)               # [list(int)]
    for i in range(len(zs)):             # [__iter(int)]
        n = 0                            # [int]
        z = zs[i]                        # [complex]
        c = cs[i]                        # [complex]
        while n < maxiter and abs(z) < 2:  # [int]
            z = z * z + c                # [complex]
            n += 1                       # [int]
        output[i] = n                    # [int]
    return output                        # [list(int)]


if __name__ == "__main__":               # []
    # make a trivial example using the correct types to enable type inference
    # call the function so ShedSkin can analyze the types
    output = calculate_z(1, [0j], [0j])  # [list(int)]
