import multiprocessing
# python -m timeit -s "import ex2_lock" "ex2_lock.run_workers()"
# 19ms using lock.acquire
# 21ms using with.lock


def work(value, max_count, lock):
    for n in range(max_count):
        with lock:
            value.value += 1
        # lock.acquire()
        #value.value += 1
        # lock.release()


def run_workers():
    NBR_PROCESSES = 4
    MAX_COUNT_PER_PROCESS = 1000
    total_expected_count = NBR_PROCESSES * MAX_COUNT_PER_PROCESS
    processes = []
    lock = multiprocessing.Lock()
    value = multiprocessing.Value('i', 0)
    for process_nbr in range(NBR_PROCESSES):
        p = multiprocessing.Process(
            target=work, args=(value, MAX_COUNT_PER_PROCESS, lock))
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
