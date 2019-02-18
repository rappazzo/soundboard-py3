from importlib import import_module

from .in_service import InService


def create(in_service_name, *args):

    try:
        if '.' in in_service_name:
            module_name, class_name = in_service_name.rsplit('.', 1)
        else:
            module_name = in_service_name
            class_name = in_service_name.capitalize()

        in_service_module = import_module('.' + module_name+"_in_service", package='in_service')

        in_service_class = getattr(in_service_module, class_name)

        instance = in_service_class(args[0])

    except (AttributeError, ModuleNotFoundError) as e:
        print (e)
        print (f"'{in_service_name}' is an unknown service")
        return None
    else:
        if not issubclass(in_service_class, InService):
            print (f"'{in_service_name}' is not a service")
            return None

    return instance

