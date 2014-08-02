import multiprocessing
# python -m timeit -s "import ex2_nolock" "ex2_nolock.run_workers()"
# 12ms


def work(value, max_count):
    for n in range(max_count):
        value.value += 1


def run_workers():
    NBR_PROCESSES = 4
    MAX_COUNT_PER_PROCESS = 1000
    total_expected_count = NBR_PROCESSES * MAX_COUNT_PER_PROCESS
    processes = []
    value = multiprocessing.Value('i', 0)
    for process_nbr in range(NBR_PROCESSES):
        p = multiprocessing.Process(
            target=work, args=(value, MAX_COUNT_PER_PROCESS))
        p.start()
        processes.append(p)

    # wait for the processes to finish
    for p in processes:
        p.join()

    # print the final value
    print "Expecting to see a count of {}".format(total_expected_count)
    print "We have counted to {}".format(value.value)

if __name__ == "__main__":
    run_workers()
