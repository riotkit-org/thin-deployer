
import unittest
import sys
import os
import inspect

sys.path.append(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..')
from thindeployer import Service


class TestCommandRunner(unittest.TestCase):
    def test_executes_commands_in_proper_order_in_proper_working_directory(self):
        result = Service.CommandRunner.run({
            'pwd': os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..',
            'commands': ['ls', 'pwd']
        }, service_name='test')

        self.assertTrue("# Deployment started: test" in result[0])
        self.assertTrue("\n\n > pwd" in result[0])

    def test_at_least_one_failure_reports_global_failure(self):
        result = Service.CommandRunner.run({
            'pwd': os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/..',
            'commands': ['pwd', 'ls /this-is-a-non-existing-directory']
        }, service_name='test')

        self.assertFalse(result[1])
