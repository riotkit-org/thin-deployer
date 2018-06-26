from tornado import web


class HelloController(web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self):
        self.write('{"message": "pong"}')
        self.add_header("X-Service-Name", "Thin Deployer")
