
from healthcheck import TornadoHandler, HealthCheck
import os
import base64


class HealthCheckController(TornadoHandler):

    """
    Provides an information about health of the service
    """

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        """
        Adds authorization to the endpoint
        :param args: 
        :param kwargs: 
        :return: 
        """

        if not self._verify_authorization():
            return

        super(HealthCheckController, self).get(*args, **kwargs)

    def _verify_authorization(self):
        token = os.getenv('HC_TOKEN')

        if self.request.headers.get('X-Auth-Token'):
            submitted_token = self.request.headers.get('X-Auth-Token')

        elif self.request.headers.get('Authorization'):
            auth_header = self.request.headers.get('Authorization')
            auth_decoded = self._decode_base64(str(auth_header))
            username, submitted_token = auth_decoded.split(':', 2)
            submitted_token = submitted_token.rstrip("'")

        else:
            self.set_header('WWW-Authenticate', 'Authentication required, put token in the password field')
            self.set_status(401)
            return False

        if not token or str(token) != submitted_token:
            self.set_status(403, "Forbidden")
            self.write({
                "message": "Not allowed to use the health check endpoint, please take a "
                           "look at HC_TOKEN environment variable"
            })
            return False

        return True

    @staticmethod
    def _decode_base64(data):
        return str(base64.b64decode(data))

    def initialize(self, checker):
        self.checker = HealthCheck(checkers=[
            self._disk_space_checker,
            self._configured_paths_exists,
            self._configured_token_too_weak
        ])

    @staticmethod
    def _disk_space_checker():
        """
        Checks if disk usage is not X% or higher, defaults to 90
        :return: 
        """

        max_percentage = int(os.getenv('HC_MAX_DISK_USAGE', 90))
        stats = os.statvfs(__file__)
        free = stats.f_frsize * stats.f_bfree
        total = stats.f_frsize * stats.f_blocks
        percentage = free/total * 100

        if percentage >= max_percentage:
            return False, "Disk usage exceeds " + str(max_percentage) + "%, actually its " + str(percentage) + "%"

        return True, "Disk usage is OK"

    def _configured_paths_exists(self):
        """
        Checks if "pwd" directories in every service is a real path
        :return: 
        """

        for service_name, config in self.application.config.items():
            if not os.path.isdir(config['pwd']):
                return False, str(service_name) + " does not have a valid path in filesystem, specified '" + str(config['pwd']) + "' does not exists"

        return True, "All services have present paths in the filesystem"

    def _configured_token_too_weak(self):
        """
        Configured token is too weak (too short for example)
        :return: 
        """

        min_token_length = int(os.getenv('HC_MIN_TOKEN_LENGTH', 16))

        for service_name, config in self.application.config.items():
            if len(config['token']) < min_token_length:
                return False, str(service_name) + " token should be at least " + str(min_token_length) + " characters, security failure"

        return True, "All tokens are at proper length"

