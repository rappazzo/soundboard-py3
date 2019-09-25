import json
import sys
import time

from command import commands
from in_service.slack_in_service import SlackConnection
from library.libraries import Libraries
from library.files_library import FilesLibrary
from concurrent.futures import ThreadPoolExecutor

from rest_service.rest_api import RestService


class Soundboard:

    def __init__(self, config_file):
        self.executor = ThreadPoolExecutor()
        with open(config_file) as f:
            self.config = json.load(f)

    def configure(self):
        # config predconditions
        lib_configs = self.config["libraries"]
        command_configs = self.config.get("commands", {})
        input_configs = self.config["input"]

        # load libraries
        for lib_config in lib_configs:
            is_default = lib_config.get("is_default", False)
            lib = FilesLibrary(lib_config["source"], lib_config.get("name", None), is_default)
            Libraries().instance.add(lib)
        Libraries().instance.ensure_default()

        # register commands

        commands.register_command("play", commands.play_sound)
        for lib in Libraries().instance.get_libs():
            if not lib.is_default():
                play_lib_cmd = lambda *sounds: commands.play_sound(lib_name=lib.get_name(), *sounds)
                commands.register_command(lib.get_name(), play_lib_cmd)

        commands.configure_commands(command_configs)
        commands.register_command("say", commands.say_phrase)
        commands.register_command("list", commands.list_sounds)
        commands.register_command("stop", commands.stop_audio)

        # register input service(s)
        if input_configs.get("slack") is not None and input_configs["slack"].get("enabled", True):
            slack_connection = SlackConnection(input_configs.get("slack"))
            slack_connection.run_service()

        if input_configs.get("rest") is not None and input_configs["rest"].get("enabled", True):
            rest = RestService(input_configs.get("rest"))
            rest.run_service()


if __name__ == "__main__":
    config = "sample-config.json"
    if len(sys.argv) > 1:
        config = sys.argv[1]

    soundboard = Soundboard(config)
    soundboard.configure()

    # wait forever
    while True:
        time.sleep(1)
