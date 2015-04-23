import datetime

from abc import ABCMeta
from abc import abstractmethod

class Epoch(metaclass = ABCMeta):
    @abstractmethod
    def epoch(self):
        return

    def __str__(self):
        return type(self).__name__


class DotNetEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1, 1, 1)


class MicrosoftEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1601, 1, 1)


class ExcelEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1899, 12, 30)


class NTPEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1900, 1, 1)


class MacOSEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1904, 1, 1)


class UnixEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1970, 1, 1)


class AOLEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1980, 1, 1)


class MacOSXEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(2001, 1, 1)
