import _util


def norm_square_list_comprehension(vector):
    return sum([v * v for v in vector])

def run_experiment(size, num_iter=3):
    vector = range(size)
    return _util.run(norm_square_list_comprehension, vector, num_iter)

if __name__ == "__main__":
    print run_experiment(1000000, 10)
