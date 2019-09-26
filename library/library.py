from abc import ABCMeta, abstractmethod


class Library(metaclass=ABCMeta):
    
    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def has_file(self, file_name):
        pass

    @abstractmethod
    def get_file(self, file_name):
        pass

    @abstractmethod
    def list(self):
        pass

    @abstractmethod
    def is_default(self):
        pass

