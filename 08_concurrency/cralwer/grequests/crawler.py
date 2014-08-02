import grequests
import string
import random


def generate_urls(base_url, num_urls):
    for i in xrange(num_urls):
        yield base_url + "".join(random.sample(string.ascii_lowercase, 10))


def run_experiment(base_url, num_iter=500):
    urls = generate_urls(base_url, num_iter)
    requests = (grequests.get(u) for u in urls)
    response_futures = grequests.imap(requests, size=100)
    response_size = sum(len(r.text) for r in response_futures)
    return response_size

if __name__ == "__main__":
    import time
    delay = 100
    num_iter = 500

    start = time.time()
    result = run_experiment(
        "http://127.0.0.1:8080/add?name=grequests&delay={}&".format(delay),
        num_iter)
    end = time.time()
    print result, (end - start)
