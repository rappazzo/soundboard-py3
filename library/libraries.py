from library.library import Library


class Libraries:
    class __Instance:
        def __init__(self):
            self.libs = {}
            self.default_lib = None

        def __str__(self):
            return repr(self)

        def add(self, lib:Library, is_default=False):
            self.libs[lib.get_name()] = lib
            if is_default:
                self.default_lib = lib

        def get_lib(self, lib_name):
            return self.libs.get(lib_name)

        def get_default_lib(self):
            return self.default_lib

        def ensure_default(self):
            if self.default_lib is None and len(self.libs) > 0:
                self.default_lib = next(self.libs)

        def get_lib_file(self, lib_name, file_name):
            lib = self.libs.get(lib_name)
            if lib is not None:
                return lib.get_file(file_name)
            return None

    instance = None

    def __init__(self):
        if not Libraries.instance:
            Libraries.instance = Libraries.__Instance()

    def __getattr__(self, name):
        return getattr(self.instance, name)

