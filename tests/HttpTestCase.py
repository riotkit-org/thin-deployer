
from tornado.testing import AsyncHTTPTestCase
import sys
import os
import inspect

sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..')
import thindeployer


class HttpTestCase(AsyncHTTPTestCase):
    def get_app(self):
        return thindeployer.create_application(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/.deployer.yml')

