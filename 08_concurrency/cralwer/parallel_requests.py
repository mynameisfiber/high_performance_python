from gevent import monkey
monkey.patch_socket()

import gevent
from gevent.coros import Semaphore
import urllib2
import string
import random
from contextlib import closing

import numpy as np
import pylab as py
from itertools import cycle
import json

markers = cycle('h*o>Dxsp8')
linestyles = cycle(['-', ':', '--', '-.'])


def generate_urls(base_url, num_urls):
    for i in xrange(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def download(url, semaphore):
    try:
        with semaphore, closing(urllib2.urlopen(url)) as data:
            return data.read()
    except Exception as e:
        print "retrying: ", e
        return download(url, semaphore)


def chunked_requests(urls, chunk_size=100):
    semaphore = Semaphore(chunk_size)
    requests = [gevent.spawn(download, u, semaphore) for u in urls]
    for response in gevent.iwait(requests):
        yield response


def run_experiment(base_url, num_iter=500, parallel_requests=100):
    urls = generate_urls(base_url, num_iter)
    response_futures = chunked_requests(urls, parallel_requests)
    response_size = sum(len(r.value) for r in response_futures)
    return response_size

if __name__ == "__main__":
    try:
        data = json.load(open("parallel_requests.json"))
    except IOError:
        import time
        delay = 100
        num_iter = 500

        data = {}
        for delay in xrange(50, 1000, 250):
            base_url = "http://127.0.0.1:8080/add?name=concurrency_test&delay={}&".format(
                delay)
            data[delay] = []
            for parallel_requests in xrange(1, num_iter, 25):
                start = time.time()
                result = run_experiment(base_url, num_iter, parallel_requests)
                t = time.time() - start
                print("{},{},{}".format(delay, parallel_requests, t))
                data[delay].append((parallel_requests, t))

        json.dump(data, open("parallel_requests.json", "w+"))
    finally:
        py.figure()
        for delay, values in data.iteritems():
            values = np.asarray(values)
            py.plot(values[:, 0], values[:, 1],
                    label="{}s request time".format(delay),
                    linestyle=linestyles.next(),
                    marker=markers.next(),
                    linewidth=4,
                    )

        py.axvline(x=100, alpha=0.5, c='r')
        ax = py.gca()
        ax.set_yscale('log')

        py.xlabel("Number of concurrent downloads")
        py.ylabel("Time to download 500 concurrent files")
        py.title("Finding the right number of concurrent requests")
        py.legend()

        py.savefig("images/parallel_requests.png")
