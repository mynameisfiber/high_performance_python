import math
import random
import time


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

nbr_samples = int(1e7)
t1 = time.time()
nbr_in_circle = estimate_nbr_points_in_circle(nbr_samples)
print "Took {}s".format(time.time() - t1)
pi_estimate = float(nbr_in_circle) / nbr_samples * 4
print "Estimated pi", pi_estimate
print "Pi", math.pi
