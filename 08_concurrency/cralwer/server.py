from tornado import httpserver
from tornado import options
from tornado import ioloop
from tornado import web
from tornado import gen

import ujson as json
import time
from collections import defaultdict

options.define("port", default=8080, help="Port to serve on")


class AddMetric(web.RequestHandler):
    metric_data = defaultdict(list)

    @gen.coroutine
    def get(self):
        if self.get_argument("flush", False):
            json.dump(self.metric_data, open("metric_data.json", "w+"))
        else:
            name = self.get_argument("name")
            try:
                delay = int(self.get_argument("delay", 1024))
            except ValueError:
                raise web.HTTPError(400, reason="Invalid value for delay")

            start = time.time()
            yield gen.Task(ioloop.IOLoop.instance().add_timeout, start + delay / 1000.)
            self.write('.')
            self.finish()
            end = time.time()
            self.metric_data[name].append({
                "start": start,
                "end": end,
                "dt": end - start,
            })


if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    application = web.Application([
        (r"/add", AddMetric),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print("Listening on port: {}".format(port))
    ioloop.IOLoop.instance().start()
