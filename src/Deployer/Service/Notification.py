
import requests
import json


class Notification:

    @staticmethod
    def send_log(output: str, webhook_url: str, title: str) -> bool:
        """
        Sends the log output to the Mattermost / Slack
        :return:
        """

        slack_data = {'text': title + ": \n\n" + output.replace('\\n', "\n") + "\n\n"}

        response = requests.post(
            webhook_url, data=json.dumps(slack_data),
            headers={'Content-Type': 'application/json'}
        )

        return response.status_code == 200
