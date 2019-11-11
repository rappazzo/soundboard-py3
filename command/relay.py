import os
import slack


relays = []


def add_relay(relayer):
    relays.append(relayer)


def send(message):
    for relayer in relays:
        relayer.relay(message)


class SlackRelay:

    def __init__(self, config=None):
        self.config = config or {}
        self.slack_token = self.config.get("token", os.environ.get("SOUNDBOARD_SLACK_TOKEN"))
        self.relay_channel = self.config.get("channel")
        if self.slack_token is None:
            print('Missing SLACK TOKEN -- disabling slack relay service')
            return
        self.client = slack.WebClient(token=self.slack_token)
        # Read bot's user ID by calling Web API method `auth.test`
        self.my_bot_id = self.client.auth_test()["user_id"]
        if self.my_bot_id is not None:
            print("Soundboard slack relay connected.")

    def relay(self, message):
        self.client.chat_postMessage(
            channel=self.relay_channel,
            as_user="true",
            text=message
        )
