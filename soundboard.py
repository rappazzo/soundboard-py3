import json
import sys
import time

import command
from command.command import register_command
from in_service.slack_in_service import SlackConnection
from library.libraries import Libraries
from library.files_library import FilesLibrary
from concurrent.futures import ThreadPoolExecutor


class Soundboard:

    def __init__(self, config_file):
        self.executor = ThreadPoolExecutor()
        with open(config_file) as f:
            self.config = json.load(f)

    def configure(self):
        # config predconditions
        lib_configs = self.config["libraries"]
        command_configs = self.config["commands"]
        input_configs = self.config["listen"]

        # load libraries
        for lib_config in lib_configs:
            lib = FilesLibrary(lib_config["source"], lib_config.get("name", None))
            is_default = lib_config.get("is_default", False)
            Libraries().instance.add(lib, is_default)
        Libraries().instance.ensure_default()

        # register commands
        for command_config in command_configs:
            command_type = command_config["type"]
            command_name = command_config["name"]
            command_args = command_config.get("args", {})
            this_command = command.create(command_type, command_args)
            register_command(command_name, this_command)

        # register input service(s)
        if input_configs.get("slack") is not None:
            slack_connection = SlackConnection(input_configs.get("slack"))
            slack_connection.run_service()
        # for input_config in input_configs:
        #     in_service_name = input_config["name"]
        #     in_service_config = input_config.get("config", {})
        #     service = in_service.create(in_service_name, in_service_config)
        #     InServices().instance.add(in_service_name, service)
        #     self.executor.submit(service.run_service)


if __name__ == "__main__":
    config = "sample-config.json"
    if len(sys.argv) > 1:
        config = sys.argv[1]

    soundboard = Soundboard(config)
    soundboard.configure()

    # wait forever
    while True:
        time.sleep(1)
