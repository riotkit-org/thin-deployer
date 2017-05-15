import tornado.web
import os
import sys
import yaml
from tornado.options import define, parse_command_line, options
from Deployer.Controller.DeployerController import DeployerController
from Deployer.Controller.HelloController import HelloController

define('configuration', default=os.path.expanduser('~/.deployer.yml'), help='Path to configuration file')

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

        for serviceName, attributes in parsed.items():
            if not "pwd" in attributes or not isinstance(attributes['pwd'], str):
                print(serviceName + '[pwd] should be a string')
                sys.exit(1)

            if not "token" in attributes or not isinstance(attributes['token'], str):
                print(serviceName + '[token] should be a string')
                sys.exit(1)

            if not "commands" in attributes or not isinstance(attributes['commands'], list):
                print(serviceName + '[commands] is not a list')
                sys.exit(1)

        self.config = parsed




def create_application():
    app = DeployerApplication([
        (r"/deploy/(?P<serviceName>[A-Za-z0-9\.\-\_]+)", DeployerController),
        (r"/", HelloController)
    ])

    app.parse_configuration()

    return app
