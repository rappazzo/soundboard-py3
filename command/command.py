from abc import ABCMeta, abstractmethod

registry = {}


class Command(metaclass=ABCMeta):

    @abstractmethod
    def invoke(self, *args):
        pass


def register_command(name: str, command: Command):
    registry[name.lower()] = command


def get_command(command_name: str):
    return registry.get(command_name.lower())


def invoke_command(command_name, *args):
    command = registry.get(command_name)
    if command is not None:
        return command.invoke(args)
    return None
