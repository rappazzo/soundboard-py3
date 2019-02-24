import os
from os import listdir
from os.path import isfile, join, splitext, isdir, split
from library.libraries import Libraries
from library.library import Library


class FilesLibrary(Library):

    location: str

    def __init__(self, location, name=None, recurse=True):
        self.location = location
        self.name = name or os.path.split(location)[1]
        self.files = {}
        self.names = []
        dirs = []
        for f in listdir(self.location):
            file = join(self.location, f)
            if isfile(file):
                f_name = os.path.splitext(f)[0]
                self.files[f_name.lower()] = file
                self.names.append(f_name)
            elif isdir(file) and recurse:
                Libraries().instance.add(FilesLibrary(file, f))

    def get_name(self):
        return self.name

    def has_file(self, file_name):
        return self.files.get(file_name.lower()) is not None

    def get_file(self, file_name):
        return self.files.get(file_name.lower())

