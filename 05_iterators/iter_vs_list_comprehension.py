import timeit
import memory_profiler
import gc


def divisible_by_three_list(numbers):
    filtered = [n for n in numbers if n % 3 == 0]
    return len(filtered)


def divisible_by_three_iterator(numbers):
    filtered = (1 for n in numbers if n % 3 == 0)
    return sum(filtered)


def memory_profile(function, *args, **kwargs):
    gc.collect()
    baseline = memory_profiler.memory_usage()[0]
    max_usage = memory_profiler.memory_usage(
        (function, args, kwargs),
        max_usage=True,
    )
    return max_usage[0] - baseline


if __name__ == "__main__":
    numbers = xrange(10000000)
    setup = "from __main__ import (numbers, " \
            "divisible_by_three_list, divisible_by_three_iterator)"
    iterations = 5

    t = timeit.timeit(
        stmt="divisible_by_three_list(numbers)",
        setup=setup,
        number=iterations,
    )
    m = memory_profile(divisible_by_three_list, numbers)
    print "divisible_by_three_list with {} entries took " \
        "{} seconds and used {} MB".format(
            len(numbers),
            t / iterations,
            m,
        )

    t = timeit.timeit(
        stmt="divisible_by_three_iterator(numbers)",
        setup=setup,
        number=iterations,
    )
    m = memory_profile(divisible_by_three_iterator, numbers)
    print "divisible_by_three_iterator with {} entries took " \
        "{} seconds and used {} MB".format(
            len(numbers),
            t / iterations,
            m,
        )
