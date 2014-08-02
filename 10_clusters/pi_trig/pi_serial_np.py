import time
import numpy as np


def y_is_in_circle(x, y):
    """Test if x,y coordinate lives within the radius of the unit circle"""
    circle_edge_y = np.sin(np.arccos(x))
    return y <= circle_edge_y


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
