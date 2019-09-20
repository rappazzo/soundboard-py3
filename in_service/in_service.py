from abc import ABCMeta, abstractmethod


class InService(metaclass=ABCMeta):
    
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def run_service(self):
        pass


