
import subprocess
import tornado.log


class CommandRunner:

    @staticmethod
    def run(service: dict, service_name: str):
        """
        Run commands for a service
        """

        output = " # Deployment started: " + service_name
        output += "\n"

        for command in service['commands']:
            tornado.log.app_log.warning('Invoking "' + command + '" in "' + service['pwd'] + '"')

            try:
                output += " > " + command
                output += str(CommandRunner.invoke_process(command, service['pwd'])) + "\n\n"

            except subprocess.CalledProcessError as exception:
                message = 'Command "' + command + '" failed, output: "' + str(exception.output) + '"'

                output += message
                tornado.log.app_log.error(message)

                return output, False

        return output, True

    @staticmethod
    def invoke_process(command: str, cwd: str):
        return str(subprocess.check_output(command, shell=True, cwd=cwd, stderr=subprocess.STDOUT))

