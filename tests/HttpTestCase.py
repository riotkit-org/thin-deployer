
from tornado.testing import AsyncHTTPTestCase
import sys
import os
import inspect

sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/../src')
import Deployer


class HttpTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return Deployer.create_application(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/.deployer.yml')

