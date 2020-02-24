import os
from math import ceil


class File:
    size = 0
    __file = 0

    def __init__(self, path):
        if self.__file == 0:
            self.__file = open(path, "rb")
            fileInfo = os.stat(path)
            self.size = format(ceil(fileInfo.st_size))

    def read(self, size):
        data = self.__file.read(size)
        return data

    def close(self):
        self.__file.close()
