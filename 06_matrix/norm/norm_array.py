from array import array
import time


def norm_square_array(vector):
    norm = 0
    for v in vector:
        norm += v * v
    return norm


def run_experiment(size, num_iter=3):
    vector = array('l', range(size))
    times = []
    for i in xrange(num_iter):
        start = time.time()
        norm_square_array(vector)
        times.append(time.time() - start)
    return min(times)

if __name__ == "__main__":
    print run_experiment(1000000, 10)
