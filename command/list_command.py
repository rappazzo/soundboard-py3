from command import Command
from library.libraries import Libraries

class List(Command):

    def __init__(self, config):
        pass

    def invoke(self, *args):
        lib = None
        lib_name = args[0]
        if lib_name is not None:
            lib = Libraries.instance.get_lib(lib_name)
        else:
            lib = Libraries.instance.get_default_lib()
        if lib is not None:
            return sorted(lib.list())
        return []
