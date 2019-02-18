from command import Command


class Commands:
    class __Instance:
        def __init__(self):
            self.commands = {}

        def __str__(self):
            return repr(self)

        def add(self, name:str, command:Command):
            self.commands[name.lower()] = command

        def get(self, command_name:str):
            return self.commands.get(command_name.lower())

        def invoke(self, command_name, *args):
            command = self.commands.get(command_name)
            if command is not None:
                return command.invoke(args)
            return None

    instance = None

    def __init__(self):
        if not Commands.instance:
            Commands.instance = Commands.__Instance()

    def __getattr__(self, name):
        return getattr(self.instance, name)

