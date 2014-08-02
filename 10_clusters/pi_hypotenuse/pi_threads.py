import math
import random
import time
#from multiprocessing.dummy import Pool
from multiprocessing import Pool


def y_is_in_circle(x, y):
    """Test if x,y coordinate lives within the radius of the unit circle"""
    return x * x + y * y <= 1.0


def estimate_nbr_points_in_circle(nbr_samples):
    nbr_in_circle = 0
    for n in xrange(nbr_samples):
        x = random.uniform(0.0, 1.0)
        y = random.uniform(0.0, 1.0)
        if y_is_in_circle(x, y):
            nbr_in_circle += 1
    return nbr_in_circle


pool = Pool()


nbr_samples = int(1e7)
nbr_parallel_blocks = 4
map_inputs = [nbr_samples] * nbr_parallel_blocks
t1 = time.time()
results = pool.map(estimate_nbr_points_in_circle, map_inputs)
# pool.close()
print results
print "Took {}s".format(time.time() - t1)
nbr_in_circle = sum(results)
combined_nbr_samples = sum(map_inputs)

pi_estimate = float(nbr_in_circle) / combined_nbr_samples * 4
print "Estimated pi", pi_estimate
print "Pi", math.pi
