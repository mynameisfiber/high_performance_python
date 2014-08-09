from array import array
import _util


def norm_square_array(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm

def run_experiment(size, num_iter=3):
    vector = array('l', range(size))
    return _util.run(norm_square_array, vector, num_iter)

if __name__ == "__main__":
    print run_experiment(1000000, 10)
