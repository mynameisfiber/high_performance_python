import gc
import time

def run(method, vector, num_iter=3):
    times = []
    for i in xrange(num_iter):
        start = time.time()
        method(vector)
        times.append(time.time() - start)
        gc.collect()
    return min(times)

