import numpy
import _util


def norm_square_numpy(vector):
    return numpy.sum(vector * vector)

def run_experiment(size, num_iter=3):
    vector = numpy.arange(size)
    return _util.run(norm_square_numpy, vector, num_iter)

if __name__ == "__main__":
    print run_experiment(1000000, 10)
