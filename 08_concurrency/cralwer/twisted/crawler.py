from twisted.internet import defer, task
from twisted.web.client import getPage

import random
import string


def generate_urls(base_url, num_urls):
    for i in range(num_urls):
        key = "".join(random.sample(string.ascii_lowercase, 10))
        yield base_url + key

BATCH_SIZE = 100
response_sum = 0


def main_task(reactor):
    def parse(data):
        global response_sum
        response_sum += len(data)

    def task_finished(*args, **kwargs):
        print args, kwargs
        print "done?"

    def fetch_urls():
        delay = 100
        num_iter = 500
        for url in generate_urls("http://127.0.0.1:8080/add?name=twisted&delay={}&".format(delay), num_iter):
            yield getPage(url).addCallback(parse)

    coop = task.Cooperator()
    urls = fetch_urls()

    return (defer.DeferredList([coop.coiterate(urls)
                                for _ in xrange(BATCH_SIZE)])
            .addCallback(task_finished))

if __name__ == "__main__":
    import time
    start = time.time()
    task.react(main_task)
    end = time.time()
    print("{} {}".format(response_sum, end - start))
