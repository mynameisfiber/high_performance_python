import requests
import grequests
import math
import time

from itertools import izip

import json


class AsyncBatcher(object):
    __slots__ = ["batch", "batch_size", "save", "flush"]

    def __init__(self, batch_size):
        self.batch_size = batch_size
        self.batch = []

    def save(self, prime):
        url = "http://127.0.0.1:8080/add?prime={}".format(prime)
        self.batch.append((url, prime))
        if len(self.batch) == self.batch_size:
            self.flush()

    def flush(self):
        responses_futures = (grequests.get(url) for url, _ in self.batch)
        responses = grequests.map(responses_futures)
        for response, (url, prime) in izip(responses, self.batch):
            finish_save_prime(response, prime)
        self.batch = []


def save_prime_serial(prime):
    url = "http://127.0.0.1:8080/add?prime={}".format(prime)
    response = requests.get(url)
    finish_save_prime(response, prime)


def finish_save_prime(response, prime):
    if response.status_code != 200:
        print "Error saving prime: {}".format(prime)


def check_prime(number):
    if number % 2 == 0:
        return False
    for i in xrange(3, int(math.sqrt(number)) + 1, 2):
        if number % i == 0:
            return False
    return True


def calculate_primes_async(max_number):
    batcher = AsyncBatcher(100)
    for number in xrange(max_number):
        if check_prime(number):
            batcher.save(number)
    batcher.flush()
    return


def calculate_primes_serial(max_number):
    for number in xrange(max_number):
        if check_prime(number):
            save_prime_serial(number)
    return


def calculate_primes_noio(max_number):
    primes = []
    for number in xrange(max_number):
        if check_prime(number):
            primes.append(number)
    return


if __name__ == "__main__":
    max_number = 100000

    try:
        data = json.load(open("primes.json"))
    except IOError:
        data = {"async": [], "serial": [], "no IO": []}
        for i in xrange(7, 15):
            max_number = 2 ** i

            start = time.time()
            calculate_primes_noio(max_number)
            t = time.time() - start
            print "noIO code took: {} {}s".format(max_number, t)
            data['no IO'].append((i, t))

            start = time.time()
            calculate_primes_async(max_number)
            t = time.time() - start
            print "Async code took: {} {}s".format(max_number, t)
            data['async'].append((i, t))

            start = time.time()
            calculate_primes_serial(max_number)
            t = time.time() - start
            print "Serial code took: {} {}s".format(max_number, t)
            data['serial'].append((i, t))
        json.dump(data, open("primes.json", "w+"))

    import pylab as py
    import numpy as np

    for name, values in data.iteritems():
        d = np.asarray(values)
        py.plot(2 ** d[:, 0], d[:, 1], label=name)

    ax = py.gca()
    ax.set_yscale('log')

    py.title("Time to find primes and save to a database")
    py.xlabel("Number of primes probed")
    py.ylabel("Time to complete")
    py.legend()
    py.savefig("images/primes.png")
