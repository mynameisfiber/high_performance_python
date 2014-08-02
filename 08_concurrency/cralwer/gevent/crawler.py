from gevent import monkey
monkey.patch_socket()

import gevent
from gevent.coros import Semaphore
import urllib2
from contextlib import closing
import string
import random


def generate_urls(base_url, num_urls):
    for i in xrange(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def download(url, semaphore):
    with semaphore, closing(urllib2.urlopen(url)) as data:
        return data.read()


def chunked_requests(urls, chunk_size=100):
    semaphore = Semaphore(chunk_size)
    requests = [gevent.spawn(download, u, semaphore) for u in urls]
    for response in gevent.iwait(requests):
        yield response


def run_experiment(base_url, num_iter=500):
    urls = generate_urls(base_url, num_iter)
    response_futures = chunked_requests(urls, 100)
    response_size = sum(len(r.value) for r in response_futures)
    return response_size

if __name__ == "__main__":
    import time
    delay = 100
    num_iter = 500
    base_url = "http://127.0.0.1:8080/add?name=gevent&delay={}&".format(delay)

    start = time.time()
    result = run_experiment(base_url, num_iter)
    end = time.time()
    print("Result: {}, Time: {}".format(result, end - start))
