import tornado.web
import tornado.log
import subprocess
import pwd
import os


class DeployerController(tornado.web.RequestHandler):

    def post(self, serviceName):
        """
        Handle input request
        :param serviceName: 
        :return: 
        """

        # get service information
        if not serviceName in self.application.config:
            self.write({'message': 'Cannot find service', 'serviceName': serviceName})
            self.set_status(404, "Not Found")

            tornado.log.app_log.warning('Tried to reach service "' + str(serviceName) + '", but its not defined')
            return

        config = self.application.config[serviceName]

        # validate authorization
        if not "X-Auth-Token" in self.request.headers or self.request.headers['X-Auth-Token'] != config['token']:
            self.write({'message': 'Invalid auth token, please verify the X-Auth-Token header value', 'serviceName': serviceName})
            self.set_status(403, "Forbidden")

            tornado.log.app_log.warning('Invalid X-Auth-Token header value for service "' + serviceName + '"')
            return

        output, is_success = self._run_commands(config, serviceName)

        # send a response
        self.set_status(202, "Accepted")
        self.add_header('X-Runs-As', pwd.getpwuid(os.getuid()).pw_name)

        if not is_success:
            self.set_status(500, "At least one step failed")

        self.write({'output': output})

        # notify
        self._notify(serviceName, output, config, is_success)

        return

    def _notify(self, service_name, output, config, is_success):
        """
        Send a notification if its enabled
        :param service_name: 
        :param output: 
        :return: 
        """

        if is_success:
            status_name = "successully"
        else:
            status_name = "with a failure"

        self.application.notification.send_log(output, config['notification_group'], '"' + service_name + '" deployment finished ' + status_name)

    def _run_commands(self, service, service_name):
        """
        Run commands for a service
        :param service: Service definition 
        :return: 
        """

        output = " # Deployment started: " + service_name
        output += "\n"

        for command in service['commands']:
            tornado.log.app_log.warning('Invoking "' + command + '" in "' + service['pwd'] + '"')

            try:
                output += " > " + command
                output += str(self._invoke_process(command, service['pwd'])) + "\n\n"
            except subprocess.CalledProcessError as exception:
                message = 'Command "' + command + '" failed, output: "' + str(exception.output) + '"'

                output += message
                tornado.log.app_log.error(message)

                return output, False

        return output, True

    def _invoke_process(self, commmand, pwd):
        return str(subprocess.check_output(commmand, shell=True, cwd=pwd))
