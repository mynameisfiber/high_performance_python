#import random
from IPython.parallel import Client, require


NBR_ESTIMATES = 1e6


# @require('NBR_ESTIMATES')  # cannot require a const

@require('random')
def calculate_pi(nbr_estimates):
    # def calculate_pi():
    #nbr_estimates = NBR_ESTIMATES

    # print "hello_world_from_ian"
    # print nbr_estimates
    #nbr_estimates = 1e6
    steps = xrange(int(nbr_estimates))
    nbr_trials_in_unit_circle = 0
    for step in steps:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_unit_circle += is_in_unit_circle

    return nbr_trials_in_unit_circle


if __name__ == "__main__":
    c = Client()
    # print c.ids
    nbr_engines = len(c.ids)
    print "We're using {} engines".format(nbr_engines)

    dview = c[:]

    # apply fn on the view's workers
    # dview.push({'NBR_ESTIMATES': NBR_ESTIMATES})  # push a global value out
    nbr_in_unit_circles = dview.apply_sync(calculate_pi, NBR_ESTIMATES)

    # apply fn with the same arg to all
    # or pass the value in locally
    #nbr_in_unit_circles = dview.apply_sync(calculate_pi, NBR_ESTIMATES)
    #nbr_jobs = 8
    #nbr_in_unit_circles = dview.map_sync(calculate_pi, [NBR_ESTIMATES] * nbr_jobs)

    print "Estimates made:", nbr_in_unit_circles

    # work using the engines only
    nbr_jobs = len(nbr_in_unit_circles)
    print sum(nbr_in_unit_circles) * 4 / NBR_ESTIMATES / nbr_jobs
