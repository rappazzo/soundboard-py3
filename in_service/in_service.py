from abc import ABCMeta, abstractmethod


class InService(metaclass=ABCMeta):
    
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def start(self, executor):
        pass


