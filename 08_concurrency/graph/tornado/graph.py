from tornado import httpserver
from tornado import options
from tornado import ioloop
from tornado import web
from tornado import gen
import tornadoredis

options.define("port", default=8080, help="Port to serve on")
rdb = None


class AddNode(web.RequestHandler):

    @gen.coroutine
    @web.asynchronous
    def get(self):
        global rdb
        node = self.get_argument("node")
        edges = self.get_arguments("edge")
        print "starting ", node
        pipeline = rdb.pipeline()
        for edge in edges:
            pipeline.sadd(node, edge)
        yield gen.Task(pipeline.execute)
        print "done ", node
        self.write("OK")
        self.finish()


@gen.coroutine
def traverse_graph(rdb, node, depth):
    links = yield gen.Task(rdb.smembers, node)
    data = {node: list(links)}
    if depth > 1:
        updates = yield [gen.Task(traverse_graph, rdb, link, depth - 1) for link in links if link not in data]
        for update in updates:
            data.update(update)
    raise gen.Return(value=data)


class ViewGraph(web.RequestHandler):

    @gen.coroutine
    @web.asynchronous
    def get(self):
        global rdb
        node = self.get_argument("node")
        try:
            depth = int(self.get_argument("depth", 1))
        except ValueError:
            raise web.HTTPError(400, reason="Invalid value for depth")

        result = yield gen.Task(traverse_graph, rdb, node, depth)
        self.write(result)
        self.finish()


if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    rdb = tornadoredis.Client()
    rdb.connect()

    application = web.Application([
        (r"/add", AddNode),
        (r"/view", ViewGraph),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print("Listening on port: {}".format(port))
    ioloop.IOLoop.instance().start()
