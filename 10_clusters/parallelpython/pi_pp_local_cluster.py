import random
import time
import pp

# http://www.parallelpython.com/content/view/18/32/
# using pp 1.6.4

# in another terminal run:
# ppserver.py -w 4 -a -d
# to setup 4 workers, autoconnect, debug logging to terminal

# running with e6420 as server and mbp in living room as worker, sent 4
# jobs but it is a 2+2 machine
#$ python pi_pp1_local_cluster.py
# Starting pp with 0 workers
# Job execution statistics:
# job count | % of all jobs | job time sum | time per job | job server
# 4 |        100.00 |     1368.6484 |   342.162107 | 192.168.0.2:60000
# Time elapsed since server creation 346.072713852
# 0 active tasks, 0 cores

# Amount of work: 400000000.0
# 3.14159028
# calculate_pi
# Delta: 346.089551926
#
# or 235 secs for 2 jobs on the MBP

#$ python pi_pp1_local_cluster.py
# Starting pp with 4 workers
# Job execution statistics:
# job count | % of all jobs | job time sum | time per job | job server
#4 |        100.00 |       0.0000 |     0.000000 | local
# Time elapsed since server creation 0.00307011604309
# 4 active tasks, 4 cores

# Job execution statistics:
# job count | % of all jobs | job time sum | time per job | job server
# 3 |         18.75 |     519.7592 |   173.253081 | 192.168.0.15:60000
#9 |         56.25 |     996.1685 |   110.685384 | local
# 4 |         25.00 |     938.5102 |   234.627538 | 192.168.0.2:60000
# Time elapsed since server creation 520.558542013
# 0 active tasks, 4 cores

# Amount of work: 1600000000.0  # 16 jobs  # note using 4 local, 2 on mbp, 1 on mbook
# 25.13313932
# calculate_pi
# Delta: 520.607908964


# Starting pp with 4 workers
# Job execution statistics:
# job count | % of all jobs | job time sum | time per job | job server
#4 |        100.00 |       0.0000 |     0.000000 | local
# Time elapsed since server creation 0.00400400161743
# 4 active tasks, 4 cores

# Job execution statistics:
# job count | % of all jobs | job time sum | time per job | job server
# 8 |         12.50 |     1405.7324 |   175.716550 | 192.168.0.15:60000
#43 |         67.19 |     4835.2221 |   112.447026 | local
# 13 |         20.31 |     2952.3180 |   227.101386 | 192.168.0.2:60000
# Time elapsed since server creation 1559.96412897
# 0 active tasks, 4 cores

# Amount of work: 6400000000.0  # 64 jobs, 2*mbp, 1*mbook
# 100.5308529
# calculate_pi
# Delta: 1560.01736903

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
    #NBR_PROCESSES = 4 + 2 + 1
    #NBR_PROCESSES = 4 + 2
    NBR_JOBS = 1  # 1024
    NBR_LOCAL_CPUS = 0
    ppservers = ("*",)  # set IP list to be auto-discovered
    # specify no local workers in this process
    job_server = pp.Server(ppservers=ppservers, ncpus=NBR_LOCAL_CPUS)

    # job_server = pp.Server(ppservers=ppservers)  # by default this would
    # enable 8 workers
    print "Starting pp with", job_server.get_ncpus(), "local workers"
    nbr_trials_per_process = [NBR_ESTIMATES] * NBR_JOBS
    t1 = time.time()
    jobs = []
    for input_args in nbr_trials_per_process:
        job = job_server.submit(calculate_pi, (input_args,), (), ("random",))
        jobs.append(job)

    job_server.print_stats()  # dump some debug info
    # each job blocks until the result is ready
    nbr_in_unit_circles = [job() for job in jobs]
    job_server.print_stats()  # dump some debug info

    processors_in_cluster = 0
    for machine_id, stats in job_server.get_stats().items():
        print "Found", machine_id
        processors_in_cluster += stats.ncpus
    print "Across the cluster we have {} CPUs".format(processors_in_cluster)

    print "Amount of work:", sum(nbr_trials_per_process)
    print "Sum of trials inside the unit circle", sum(nbr_in_unit_circles)
    print sum(nbr_in_unit_circles) * 4 / NBR_JOBS / NBR_ESTIMATES
    print calculate_pi.func_name
    overall_time = time.time() - t1
    print "Delta:", overall_time
    print "Average time", overall_time / NBR_JOBS
