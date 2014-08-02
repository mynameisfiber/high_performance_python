import time
import numpy as np
import numexpr


def y_is_in_circle(x, y):
    """Test if x,y coordinate lives within the radius of the unit circle"""
    return numexpr.evaluate("x*x+y*y <= 1.0")


nbr_samples = int(1e7)
xs = np.random.uniform(size=nbr_samples)
ys = np.random.uniform(size=nbr_samples)
t1 = time.time()
nbr_in_circle = y_is_in_circle(xs, ys)
print "Took {}s".format(time.time() - t1)
nbr_in_circle = float(np.sum(nbr_in_circle))
print nbr_in_circle

pi_estimate = nbr_in_circle / nbr_samples * 4
print pi_estimate
print np.pi
