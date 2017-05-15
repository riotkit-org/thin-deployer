import tornado.web
import tornado.log
import subprocess
import json
import pwd
import os

class DeployerController(tornado.web.RequestHandler):

    def post(self, serviceName):
        """
        Handle input request
        :param serviceName: 
        :return: 
        """

        if not serviceName in self.application.config:
            self.write(json.dumps({'message': 'Cannot find service', 'serviceName': serviceName}))
            self.set_status(404, "Not Found")

            tornado.log.app_log.warning('Tried to reach service "' + str(serviceName) + '", but its not defined')
            return

        config = self.application.config[serviceName]

        if not "X-Auth-Token" in self.request.headers or self.request.headers['X-Auth-Token'] != config['token']:
            self.write(json.dumps({'message': 'Invalid auth token, please verify the X-Auth-Token header value', 'serviceName': serviceName}))
            self.set_status(403, "Forbidden")

            tornado.log.app_log.warning('Invalid X-Auth-Token header value for service "' + serviceName + '"')
            return

        output = self._run_commands(config)

        self.set_status(202, "Accepted")
        self.add_header('X-Runs-As', pwd.getpwuid(os.getuid()).pw_name)
        self.write(json.dumps({'output': output}))

        return

    def _run_commands(self, service):
        """
        Run commands for a service
        :param service: Service definition 
        :return: 
        """

        output = ""

        for command in service['commands']:
            tornado.log.app_log.warning('Invoking "' + command + '" in "' + service['pwd'] + '"')
            output += str(self._invoke_process(command, service['pwd']))

        return output


    def _invoke_process(self, commmand, pwd):
        return str(subprocess.check_output(commmand, shell=True, cwd=pwd))
