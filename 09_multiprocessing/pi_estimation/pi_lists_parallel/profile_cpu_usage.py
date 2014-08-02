import time
import numpy as np
import psutil
from matplotlib import pyplot as plt
import subprocess
import argparse
import cPickle


SHRINK = 1  # fraction to shrink colorbar by if it overextends


# SLEEP_FOR = 15  # seconds
#xargs = ["python", "pi_lists_parallel.py", "1", "--processes"]

# SLEEP_FOR = 7  # seconds
#xargs = ["python", "pi_lists_parallel.py", "2", "--processes"]

# SLEEP_FOR = 3  # seconds
#xargs = ["python", "pi_lists_parallel.py", "4", "--processes"]

# SLEEP_FOR = 3  # seconds
#xargs = ["python", "pi_lists_parallel.py", "8", "--processes"]

# thread version
# SLEEP_FOR = 20  # seconds
#args = ["python", "pi_lists_parallel.py", "4"]
# SLEEP_FOR = 2  # seconds
#args = ["python", "pi_lists_parallel.py", "4", "--nbr_samples_in_total=10000000"]

# threaded numpy workers
# SLEEP_FOR = 0.4  # seconds
#args = ["python", "../pi_processes_parallel/pi_numpy_parallel_worker.py", "1"]

# SLEEP_FOR = 0.4  # seconds
#args = ["python", "../pi_processes_parallel/pi_numpy_parallel_worker.py", "8"]


# generate the data
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project description')
    parser.add_argument('--build', action="store_true",
                        default=False, help='required positional argument')
    parser.add_argument('--processes', action="store_true",
                        default=False, help='required positional argument')
    parser.add_argument(
        '--nbr_processes',
        default=1,
        type=int,
        help='required positional argument')
    args = parser.parse_args()

    xargs = ["python", "pi_lists_parallel.py"]
    xargs.append(str(args.nbr_processes))
    if args.processes:
        xargs.append("--processes")
        SLEEP_FOR = {8: 3, 4: 4, 2: 7, 1: 15}[args.nbr_processes]
    else:
        print "THREADED VERSION"
        SLEEP_FOR = {4: 20}[args.nbr_processes]

    print "Using:", xargs

    ROOT_NAME = "08_" + "_".join(
        s.replace(
            "-",
            "").replace(
            ".",
            "_").replace(
                "=",
                "_").replace(
                    "/",
                    "_") for s in xargs[
                        1:])
    print ROOT_NAME
    PICKLE_NAME = ROOT_NAME + ".pickle"
    FIG_NAME = ROOT_NAME + ".png"

    if args.build:

        sts = subprocess.Popen(xargs)
        t = 0
        time_labels = []
        while True:
            # [27.3, 90.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            percents_now = psutil.cpu_percent(percpu=True)
            percents_now.sort(reverse=True)
            if t == 0:
                percents = np.array([percents_now])  # , dtype=np.float_)
            else:
                percents = np.append(percents, [percents_now], axis=0)

            time_labels.append(str(t))

            # break when workers are finished
            time.sleep(SLEEP_FOR)
            if sts.poll() >= 0:
                break
            t += SLEEP_FOR

        cPickle.dump((percents, time_labels), open(PICKLE_NAME, 'w'))
    else:
        # generate the plots
        (percents, time_labels) = cPickle.load(open(PICKLE_NAME, 'r'))

        f = plt.figure()

        # cmap='hot' looks lovely on color screens
        plt.imshow(
            percents.T, interpolation='nearest', cmap='binary', origin='lower')
        plt.xlabel('time (seconds)')
        plt.ylabel('CPU (4 cores and 4 HyperThreads)')
        plt.title("CPU usage over time")
        # max sure we plot 0..100% even if cpu doesn't get to 100% usage
        plt.clim(0, 100)
        plt.yticks(np.arange(-0.5, 8.5), np.arange(1, 9))
        plt.xticks(np.arange(-0.5, len(percents)), time_labels)

        cb = plt.colorbar(shrink=SHRINK)
        cb.set_label("CPU %")

        plt.draw()
        plt.tight_layout()
        plt.savefig(FIG_NAME)
