from in_service import InService


class InServices:
    class __Instance:
        def __init__(self):
            self.in_services = {}

        def __str__(self):
            return repr(self)

        def add(self, name, in_service:InService):
            self.in_services[name] = in_service

        def get(self, in_service_name):
            return self.in_services.get(in_service_name)

    instance = None

    def __init__(self):
        if not InServices.instance:
            InServices.instance = InServices.__Instance()

    def __getattr__(self, name):
        return getattr(self.instance, name)

