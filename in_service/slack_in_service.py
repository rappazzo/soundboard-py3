import os
import time
import re
import sys
from slack import WebClient

import command
from command.commands import Commands
from in_service import InService

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
MENTION_REGEX = "<@(|[WU].+?)> `?(.*?)`?"


class Slack(InService):

    def __init__(self, config={}):
        self.slack_token = config.get("token", os.environ["SOUNDBOARD_SLACK_TOKEN"])
        self.slack_client = WebClient(token=self.slack_token)
        self.soundboard_bot_id = None

    def get_name(self):
        return "slack"

    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.

            If the channel stars with:
             - C, it's a public channel
             - D, it's a DM with the user
             - G, it's either a private channel or multi-person DM
        """
        for event in slack_events:
            if event["type"] == "message" and "subtype" not in event and not event["user"] == self.soundboard_bot_id:
                # print (event)
                if event["channel"][0] == 'D':
                    # direct message
                    # print ("   Direct Message")
                    return event["text"], event["channel"], event["user"]

                else:
                    user_id, message = Slack.parse_direct_mention(event["text"])
                    if user_id == self.soundboard_bot_id:
                        return message, event["channel"], event["user"]
        return None, None, None

    @staticmethod
    def parse_direct_mention(message_text):
        """
            Finds a direct mention in message text and returns the user ID which
            was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def format_command_response(self, cmd_response):
        response = None
        if isinstance(cmd_response, str):
            response = cmd_response
        else:
            # treat as a list -- join list items with \n
            response = "\n".join(cmd_response)
        return response

    def handle_command(self, message, channel, user):
        """
            Executes bot command if the command is known
        """

        # Default response is help text for the user
        default_response = f"I don't understand {message}.  Perhaps you want *help*?"

        # Finds and executes the given command, filling in response
        response = None

        command_and_args = message.split(maxsplit=1)
        command_name = command_and_args[0]
        args = None
        if len(command_and_args) > 1:
            args = command_and_args[1]

        try:
            command = Commands().instance.get(command_name)
            if command is not None:
                response = self.format_command_response(command.invoke(args))
                if len(response) > 100:
                    response = f"```{response}```"
        except NameError as e:
            print(e)

        # Sends the response back to the channel
        if response is None or len(response) > 400:
            channel = user
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            as_user="true",
            text=response or default_response
        )

    def connect(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print("Soundboard slack bot connected and running!")
            # Read bot's user ID by calling Web API method `auth.test`
            self.soundboard_bot_id = self.slack_client.api_call("auth.test")["user_id"]
            return self.soundboard_bot_id is not None
        else:
            print("Slack connection failed!")
        return False

    def monitor(self):
        while True:
            command, channel, user = self.parse_bot_commands(self.slack_client.rtm_read())
            if command:
                self.handle_command(command, channel, user)
            time.sleep(RTM_READ_DELAY)

    def connect_and_monitor(self):
        if self.connect():
            self.monitor()

    def start(self, executor):
        executor.submit(self.connect_and_monitor)


# Main
if __name__ == "__main__":
    from command.commands import Commands
    from library.libraries import Libraries
    from library.files_library import FilesLibrary
    Libraries().instance.add(FilesLibrary('/Users/mike/Library/Audio/Sounds/soundboard'), is_default=True)
    Commands().instance.add(command.create("play", {}))
    Commands().instance.add(command.create("list", {}))
    slack = Slack()
    slack.connect_and_monitor()
