import os
import re
import sys

import slack

from command import commands
from in_service import InService

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
MENTION_REGEX = "<@(|[WU].+?)> `?(.*?)`?"
who_cache = {}


class SlackConnection(InService):

    def __init__(self, config=None):
        self.config = config or {}
        self.slack_token = self.config.get("token", os.environ.get("SOUNDBOARD_SLACK_TOKEN"))
        if self.slack_token is None:
            print('Missing SLACK TOKEN -- disabling slack listener service')
            return
        self.rtm = slack.RTMClient(token=self.slack_token, run_async=True)
        self.client = slack.WebClient(token=self.slack_token)
        # Read bot's user ID by calling Web API method `auth.test`
        self.my_bot_id = self.client.auth_test()["user_id"]

    def get_name(self):
        return "slack"

    def relay(self):
        pass

    @staticmethod
    def format_command_response(cmd_response):
        if isinstance(cmd_response, str):
            response = cmd_response
        else:
            try:
                response = "\n".join(cmd_response)
            except TypeError:
                response = cmd_response
        return response

    def handle_command(self, message, payload):
        """
            Executes bot command if the command is known
        """

        # Default response is help text for the user
        default_response = f"I don't understand {message}.  Perhaps you want *help*?"

        # Finds and executes the given command, filling in response
        response = None

        if message == "stop listening":
            self.rtm.stop()
            sys.exit(0)

        command_and_args = message.split(maxsplit=1)
        command_name = command_and_args[0]
        args = None
        if len(command_and_args) > 1:
            args = command_and_args[1]

        try:
            cmd = commands.get_command(command_name)
            if cmd is not None:
                who = self.get_who(payload)
                response = self.format_command_response(cmd(args, who=who))
                if len(response) > 100:
                    response = f"```{response}```"
        except NameError as e:
            print(e)

        # Sends the response back to the channel
        if response is None or len(response) > 400:
            channel = payload['data']['user']
        else:
            channel = payload['data']['channel']

        payload['web_client'].chat_postMessage(
            # thread_ts=payload['data']['ts'], <-- threaded?
            channel=channel,
            as_user="true",
            text=response or default_response
        )

    def get_who(self, payload):
        who = payload['data']['user']
        who_data = who_cache.get(who)
        if who_data is None:
            who_data = self.client.users_info(user=who)
            if who_data is not None and who_data["ok"]:
                who_cache[who] = who_data["user"]
                who = who_cache[who]["real_name"]
        else:
            who = who_data["real_name"]
        return who

    def handle_message(self, **payload):
        """
            Executes bot command if the command is known
        """
        data = payload['data']
        # Ignore messages posted by this bot
        user = data.get('user')
        if user == self.my_bot_id:
            return

        message = data.get("text")
        if message is None:
            return

        if data['channel'][0] == 'D':
            # direct message
            # print ("   Direct Message")
            self.handle_command(message, payload)
        else:
            user_id, message = parse_direct_mention(message)
            if user_id == self.my_bot_id:
                self.handle_command(message, payload)

    def run_service(self):
        slack.RTMClient.run_on(event='message')(self.handle_message)
        if self.my_bot_id is not None:
            print("Soundboard slack bot connected and running!")
            self.rtm.start()
        else:
            print("Slack connection failed!")

    def stop_service(self):
        self.rtm.stop()


def parse_direct_mention(message_text):
    """
        Finds a direct mention in message text and returns the user ID which
        was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


# Main
if __name__ == "__main__":
    from library.libraries import Libraries
    from library.files_library import FilesLibrary
    Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
    commands.register_command("play", commands.play_sound)
    commands.register_command("list", commands.list_sounds)
    slack_connection = SlackConnection()
    slack_connection.run_service()
