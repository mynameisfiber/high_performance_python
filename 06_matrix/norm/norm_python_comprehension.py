import time

def norm_square_list_comprehension(vector):
    return sum([v*v for v in vector])

def run_experiment(size, num_iter=3):
    vector = range(size)
    times = []
    for i in xrange(num_iter):
        start = time.time()
        norm_square_list_comprehension(vector)
        times.append(time.time() - start)
    return min(times)

if __name__ == "__main__":
    print run_experiment(1000000, 10)

