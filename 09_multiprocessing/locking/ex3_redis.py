import multiprocessing
import redis
# python -m timeit -s "import ex3_redis" "ex3_redis.run_workers()"
# 81 ms


rds = redis.StrictRedis()
REDIS_KEY = "ex3_redis_key"


def work(max_count):
    for n in range(max_count):
        rds.incr(REDIS_KEY)


def run_workers():
    NBR_PROCESSES = 4
    MAX_COUNT_PER_PROCESS = 1000
    total_expected_count = NBR_PROCESSES * MAX_COUNT_PER_PROCESS

    rds[REDIS_KEY] = 0

    processes = []
    for process_nbr in range(NBR_PROCESSES):
        p = multiprocessing.Process(target=work, args=(MAX_COUNT_PER_PROCESS,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    # print the final value
    print "Expecting to see a count of {}".format(total_expected_count)
    print "We have counted to {}".format(rds[REDIS_KEY])


if __name__ == "__main__":
    run_workers()
