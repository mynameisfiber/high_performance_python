from tornado import ioloop
from tornado.httpclient import AsyncHTTPClient

from functools import partial
import string
import random

AsyncHTTPClient.configure(
    "tornado.curl_httpclient.CurlAsyncHTTPClient", max_clients=100)


def generate_urls(base_url, num_urls):
    for i in xrange(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def fetch_urls(urls, callback):
    http_client = AsyncHTTPClient()
    urls = list(urls)
    responses = []

    def _finish_fetch_urls(result):
        responses.append(result)
        if len(responses) == len(urls):
            callback(responses)
    for url in urls:
        http_client.fetch(url, callback=_finish_fetch_urls)


def run_experiment(base_url, num_iter=500, callback=None):
    urls = generate_urls(base_url, num_iter)
    callback_passthrou = partial(_finish_run_experiment,
                                 callback=callback)
    fetch_urls(urls, callback_passthrou)


def _finish_run_experiment(responses, callback):
    response_sum = sum(len(r.body) for r in responses)
    print response_sum
    callback()

if __name__ == "__main__":
    import time
    delay = 100
    num_iter = 500
    base_url = "http://127.0.0.1:8080/add?name=tornado_callback&delay={}&".format(
        delay)

    _ioloop = ioloop.IOLoop.instance()
    _ioloop.add_callback(run_experiment, base_url, num_iter, _ioloop.stop)

    start = time.time()
    _ioloop.start()
    end = time.time()
    print (end - start)
