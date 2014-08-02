from tornado import httpserver
from tornado import options
from tornado import ioloop
from tornado import web
import redis

options.define("port", default=8080, help="Port to serve on")
rdb = None


class AddNode(web.RequestHandler):

    def get(self):
        global rdb
        node = self.get_argument("node")
        edges = self.get_arguments("edge")
        for edge in edges:
            rdb.sadd(node, edge)
        self.write("OK")
        self.finish()


def traverse_graph(rdb, node, depth):
    links = rdb.smembers(node)
    data = {node: list(links)}
    if depth > 1:
        for link in links:
            if link not in data:
                data.update(traverse_graph(rdb, link, depth - 1))
    return data


class ViewGraph(web.RequestHandler):

    def get(self):
        global rdb
        node = self.get_argument("node")
        try:
            depth = int(self.get_argument("depth", 1))
        except ValueError:
            raise web.HTTPError(400, reason="Invalid value for depth")

        result = traverse_graph(rdb, node, depth)
        self.write(result)
        self.finish()


if __name__ == "__main__":
    options.parse_command_line()
    port = options.options.port

    rdb = redis.StrictRedis()
    application = web.Application([
        (r"/add", AddNode),
        (r"/view", ViewGraph),
    ])

    http_server = httpserver.HTTPServer(application)
    http_server.listen(port)
    print("Listening on port: {}".format(port))
    ioloop.IOLoop.instance().start()
