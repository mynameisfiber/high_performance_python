import random
import string
import timeit


def list_unique_names(phonebook):
    unique_names = []
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        for unique in unique_names:
            if unique == first_name:
                break
        else:
            unique_names.append(first_name)
    return len(unique_names)


def set_unique_names(phonebook):
    unique_names = set()
    for name, phonenumber in phonebook:
        first_name, last_name = name.split(" ", 1)
        unique_names.add(first_name)
    return len(unique_names)


def random_name():
    first_name = "".join(random.sample(string.ascii_letters, 8))
    last_name = "".join(random.sample(string.ascii_letters, 8))
    return "{} {}".format(first_name, last_name)

if __name__ == "__main__":
    phonebook = [
        ("John Doe", "555-555-5555"),
        ("Albert Einstein", "212-555-5555"),
        ("John Murphey", "202-555-5555"),
        ("Albert Rutherford", "647-555-5555"),
        ("Elaine Bodian", "301-555-5555"),
    ]

    print "Number of unique names from set method:", set_unique_names(phonebook)
    print "Number of unique names from list method:", list_unique_names(phonebook)

    setup = "from __main__ import (large_phonebook, set_unique_names, list_unique_names)"
    iterations = 50
    large_phonebook = [
        (random_name(), "555-555-5555")
        for i in xrange(1000)
    ]

    t = timeit.timeit(
        stmt="list_unique_names(large_phonebook)",
        setup=setup,
        number=iterations
    )
    print "Finding unique names in a phonebook of length {} using lists " \
        "took: {:2e} seconds".format(len(large_phonebook), t / iterations)

    t = timeit.timeit(
        stmt="set_unique_names(large_phonebook)",
        setup=setup,
        number=iterations
    )
    print "Finding unique names in a phonebook of length {} using sets " \
        "took:  {:2e} seconds".format(len(large_phonebook), t / iterations)
