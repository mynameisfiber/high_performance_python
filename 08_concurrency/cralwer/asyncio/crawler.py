#!/usr/bin/env python3

import asyncio
import aiohttp
import random
import string


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def chunked_http_client(num_chunks):
    semaphore = asyncio.Semaphore(num_chunks)

    @asyncio.coroutine
    def http_get(url):
        nonlocal semaphore
        with (yield from semaphore):
            response = yield from aiohttp.request('GET', url)
            body = yield from response.content.read()
            yield from response.wait_for_close()
        return body
    return http_get


def run_experiment(base_url, num_iter=500):
    urls = generate_urls(base_url, num_iter)
    http_client = chunked_http_client(100)
    tasks = [http_client(url) for url in urls]
    responses_sum = 0
    for future in asyncio.as_completed(tasks):
        data = yield from future
        responses_sum += len(data)
    return responses_sum

if __name__ == "__main__":
    import time
    loop = asyncio.get_event_loop()
    delay = 100
    num_iter = 500

    start = time.time()
    result = loop.run_until_complete(
        run_experiment(
            "http://127.0.0.1:8080/add?name=asyncio&delay={}&".format(delay),
            num_iter))
    end = time.time()
    print("{} {}".format(result, end - start))
