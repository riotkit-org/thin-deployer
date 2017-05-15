from tornado import web

class HelloController(web.RequestHandler):

    def get(self):
        self.write('{"message": "pong"}')
        self.add_header("X-Service-Name", "Thin Deployer")
