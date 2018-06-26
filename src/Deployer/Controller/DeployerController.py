
import tornado.web
import tornado.log
from .. import Service
import pwd
import os
import re


class DeployerController(tornado.web.RequestHandler):

    def data_received(self, chunk):
        pass

    def get(self, service_name):
        return self.post(service_name)

    def post(self, service_name):
        """
        Handle input request
        """

        # get service information
        if service_name not in self.application.config:
            self.write({'message': 'Cannot find service', 'serviceName': service_name})
            self.set_status(404, "Not Found")

            tornado.log.app_log.warning('Tried to reach service "' + str(service_name) + '", but its not defined')
            return

        config = self.application.config[service_name]

        if not self._assert_has_access(service_name, config):
            return

        if not self._validate_request(config):
            self.set_status(200, "OK")
            return

        output, is_success = Service.CommandRunner.run(config, service_name)

        # send a response
        self.set_status(202, "Accepted")
        self.add_header('X-Runs-As', pwd.getpwuid(os.getuid()).pw_name)

        if not is_success:
            self.set_status(500, "At least one step failed")

        self.write({'output': output})

        # notify
        self._notify(service_name, output, config, is_success)

        return

    def _validate_request(self, config: dict):
        """
        Check if the request body contains a match of a regexp
        """
        if "request_regexp" in config:
            if not len(re.findall(config['request_regexp'], str(self.request.body))) > 0:
                self.set_status(200, "OK")
                self.write({'output': 'Request validation returned a status that there is no need to deploy'})
                return False

        return True

    def _notify(self, service_name: str, output: str, config: dict, is_success: bool):
        """
        Send a notification if its enabled
        """

        if not config['use_notification']:
            return

        if is_success:
            status_name = "successfully"
        else:
            status_name = "with a failure"

        self.application.notification.send_log(
            output,
            config['notification_group'],
            '"' + service_name + '" deployment finished ' + status_name
        )

    def _assert_has_access(self, service_name: str, config: dict):
        if "X-Auth-Token" in self.request.headers and self.request.headers['X-Auth-Token'] == config['token']:
            return True

        if self.get_argument("token", None, True) == config['token']:
            return True

        self.write({
            'message': 'Invalid auth token, please verify the X-Auth-Token header value or "token" query parameter',
            'serviceName': service_name
        })

        self.set_status(403, "Forbidden")
        tornado.log.app_log.warning('Invalid X-Auth-Token header value, and/or token query parameter for service '
                                    '"' + service_name + '"')
        return False
