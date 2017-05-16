
import subprocess

class Notification:
    def send_log(self, output, group_name, title):
        """
        Sends the log output to the Wolnościowiec Notification using the shell client
        :param output: 
        :return: 
        """

        ps = subprocess.Popen(('echo', output), stdout=subprocess.PIPE)
        output = subprocess.check_output(('notification-message-send', '-g', group_name, '-t', 'Thin Deployer: ' + title), stdin=ps.stdout)
        ps.wait()

        return output