from importlib import import_module

from .command import Command


def create(command_name, *args):

    try:
        if '.' in command_name:
            module_name, class_name = command_name.rsplit('.', 1)
        else:
            module_name = command_name
            class_name = command_name.capitalize()

        command_module = import_module('.' + module_name+"_command", package='command')

        command_class = getattr(command_module, class_name)

        instance = command_class(args[0])

    except (AttributeError, ModuleNotFoundError) as e:
        print (e)
        print (f"'{command_name}' is an unknown command")
        return None
    else:
        if not issubclass(command_class, Command):
            print (f"'{command_name}' is not a Command")
            return None

    return instance
