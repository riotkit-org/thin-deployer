
import tornado.web
import tornado.log
import os
import sys
import yaml
from tornado.options import define, parse_command_line, options
import tornado.ioloop

from .Controller.DeployerController import DeployerController
from .Controller.HelloController import HelloController
from .Controller.HealthCheckController import HealthCheckController
from .Service.Notification import Notification


define('configuration', default=os.path.expanduser('~/.deployer.yml'), help='Path to configuration file', type=str)
define('port', default=8012, help='Port to listen on', type=int)
define('listen', default='', help='IP address to listen on, defaults to 0.0.0.0 to listen on all ports', type=str)

parse_command_line()


class DeployerApplication(tornado.web.Application):
    config = {}

    def parse_configuration(self, path=None):
        """
            Parse configuration YAML file
            (validates before proceeding)
            
            The configuration array is accessible via self.config
        """

        # fallback to default path (~/.deployer.yml)
        if not path:
            path = os.path.expanduser(options.configuration)

        # when a directory was specified to be included
        if os.path.isdir(str(path)):
            for filename in os.listdir(path):
                if os.path.isfile(path + '/' + filename) and filename.endswith('.yml'):
                    self.parse_configuration(path + '/' + filename)

            return

        if not os.path.isfile(str(path)):
            tornado.log.app_log.error('File "' + str(path) + '" not found')
            sys.exit(1)

        tornado.log.app_log.info('Parsing ' + path)

        pointer = open(path, "r")
        parsed = yaml.load(pointer)
        pointer.close()

        if not isinstance(parsed, dict) or len(parsed) == 0:
            tornado.log.app_log.error('Empty configuration or not a dictionary on top level')
            sys.exit(1)

        node_definition = {
            'pwd': str,
            'token': str,
            'use_notification': bool,
            'notification_webhook_url': str,
            'commands': list,
            'request_regexp': str
        }

        for serviceName, attributes in parsed.items():

            if "include" in attributes:
                return self.parse_configuration(path=attributes['include'])

            for attribute_name, class_type in node_definition.items():
                if not attribute_name in attributes or not isinstance(attributes[attribute_name], class_type):
                    print(serviceName + '[' + attribute_name + '] should be of a ' + str(class_type.__name__) + ' type')
                    sys.exit(1)

            self.config[serviceName] = attributes

    def initialize(self):
        self.notification = Notification()


def create_application(path=None):
    app = DeployerApplication([
        (r"/deploy/(?P<service_name>[A-Za-z0-9\.\-\_]+)", DeployerController),
        (r"/technical/healthcheck", HealthCheckController, dict(checker="")),
        (r"/", HelloController)
    ])

    app.parse_configuration(path)
    app.initialize()

    return app


def run_application():
    app = create_application()
    app.listen(options.port, options.listen)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    run_application()
