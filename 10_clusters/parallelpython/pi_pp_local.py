import random
import time
import pp

# http://www.parallelpython.com/content/view/18/32/
# using pp 1.6.4

#NBR_ESTIMATES = 1e8
NBR_ESTIMATES = 1e8


def calculate_pi(nbr_estimates):
    steps = xrange(int(nbr_estimates))
    nbr_trials_in_unit_circle = 0
    for step in steps:
        x = random.uniform(0, 1)
        y = random.uniform(0, 1)
        is_in_unit_circle = x * x + y * y <= 1.0
        nbr_trials_in_unit_circle += is_in_unit_circle

    return nbr_trials_in_unit_circle


if __name__ == "__main__":
    NBR_PROCESSES = 4
    job_server = pp.Server(ncpus=NBR_PROCESSES)
    print "Starting pp with", job_server.get_ncpus(), "workers"
    nbr_trials_per_process = [NBR_ESTIMATES] * NBR_PROCESSES
    t1 = time.time()
    jobs = []
    for input_args in nbr_trials_per_process:
        job = job_server.submit(calculate_pi, (input_args,), (), ("random",))
        jobs.append(job)
    # each job blocks until the result is ready
    nbr_in_unit_circles = [job() for job in jobs]
    print "Amount of work:", sum(nbr_trials_per_process)
    print sum(nbr_in_unit_circles) * 4 / NBR_ESTIMATES / NBR_PROCESSES
    print calculate_pi.func_name
    print "Delta:", time.time() - t1
