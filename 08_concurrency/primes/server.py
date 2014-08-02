from tornado import httpserver
from tornado import options
from tornado import ioloop
from tornado import web
from tornado import gen

import time

options.define("port", default=8080, help="Port to serve on")
primes = set()


class AddPrime(web.RequestHandler):

    @gen.coroutine
    def get(self):
        prime = int(self.get_argument("prime"))
        primes.add(prime)
        restart_time = time.time() + .050
        yield gen.Task(ioloop.IOLoop.instance().add_timeout, restart_time)
        self.write(".")
        self.finish()

if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    application = web.Application([
        (r"/add", AddPrime),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print("Listening on port: {}".format(port))
    ioloop.IOLoop.instance().start()
