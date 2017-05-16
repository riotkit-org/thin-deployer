
import tornado.web
import os
import sys
import yaml
from tornado.options import define, parse_command_line, options
from Deployer.Controller.DeployerController import DeployerController
from Deployer.Controller.HelloController import HelloController
from Deployer.Service.Notification import Notification

define('configuration', default=os.path.expanduser('~/.deployer.yml'), help='Path to configuration file', type=str)
define('port', default=8012, help='Port to listen on', type=int)
define('listen', default='', help='IP address to listen on, defaults to 0.0.0.0 to listen on all ports', type=str)

parse_command_line()

class DeployerApplication(tornado.web.Application):

    config = {}

    def parse_configuration(self):
        """
            Parse configuration YAML file
            (validates before proceeding)
            
            The configuration array is accessible via self.config
        """

        path = os.path.expanduser(options.configuration)

        if not os.path.isfile(path):
            print('File "' + path + '" not found')
            sys.exit(1)

        pointer = open(path, "r")
        parsed = yaml.load(pointer)
        pointer.close()

        if not isinstance(parsed, dict) or len(parsed) == 0:
            print('Empty configuration or not a dictionary on top level')
            sys.exit(1)

        node_definition = {
            'pwd': str,
            'token': str,
            'use_notification': bool,
            'notification_group': str,
            'commands': list
        }

        for serviceName, attributes in parsed.items():
            for attribute_name, class_type in node_definition.items():
                if not attribute_name in attributes or not isinstance(attributes[attribute_name], class_type):
                    print(serviceName + '[' + attribute_name + '] should be of a ' + str(class_type.__name__) + ' type')
                    sys.exit(1)


        self.config = parsed

    def initialize(self):
        self.notification = Notification()


def create_application():
    app = DeployerApplication([
        (r"/deploy/(?P<serviceName>[A-Za-z0-9\.\-\_]+)", DeployerController),
        (r"/", HelloController)
    ])

    app.parse_configuration()
    app.initialize()

    return app
