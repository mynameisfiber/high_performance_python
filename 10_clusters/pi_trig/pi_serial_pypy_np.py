import time
import numpy as np

# numpy works sort-of inside pypy
# random_sample replaces uniform (it has a half-open interval, not fully open)
# np.sum does not work the same as sum
# http://morepypy.blogspot.co.uk/2013/11/numpy-status-update.html
# http://buildbot.pypy.org/numpy-status/latest.html


def y_is_in_circle(x, y):
    """Test if x,y coordinate lives within the radius of the unit circle"""
    circle_edge_y = np.sin(np.arccos(x))
    return y <= circle_edge_y


nbr_samples = int(1e7)
print "Using:", nbr_samples
xs = np.random.random_sample(size=nbr_samples)
ys = np.random.random_sample(size=nbr_samples)
t1 = time.time()
nbr_in_circle = y_is_in_circle(xs, ys)
print "Took {}s".format(time.time() - t1)
print nbr_in_circle[:10]
nbr_in_circle_sum = float(sum(nbr_in_circle))
print nbr_in_circle_sum

pi_estimate = nbr_in_circle_sum / nbr_samples * 4
print pi_estimate
print np.pi
