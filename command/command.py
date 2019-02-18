from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):

    @abstractmethod
    def invoke(self, *args):
        pass

