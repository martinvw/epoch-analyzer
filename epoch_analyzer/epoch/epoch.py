import datetime

from abc import ABCMeta
from abc import abstractmethod

class Epoch(metaclass = ABCMeta):
    """Explanations are (unless stated otherwise) from http://en.wikipedia.org/wiki/Epoch_(reference_data)"""
    @abstractmethod
    def epoch(self):
        """ this method should be implemented in one of the childs. """


    def __str__(self):
        return type(self).__name__ + "("+str(self.epoch().date())+")"


class DotNetEpoch(Epoch):
    """Based on ISO 2014 and RFC 3339"""
    def epoch(self):
        return datetime.datetime(1, 1, 1)


class MicrosoftEpoch(Epoch):
    """1601 was the first year of the 400-year Gregorian calender cycle at the
        time Windows NT was made"""
    def epoch(self):
        return datetime.datetime(1601, 1, 1)


class ExcelEpoch(Epoch):
    """Technical internal value used by Microsoft Excel; for compatibility with
        Lotus 1-2-3."""
    def epoch(self):
        return datetime.datetime(1899, 12, 30)


class NTPEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1900, 1, 1)


class MacOSEpoch(Epoch):
    """1904 is the first leap year of the 20th century"""
    def epoch(self):
        return datetime.datetime(1904, 1, 1)


class UnixEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1970, 1, 1)


class FATEpoch(Epoch):
    def epoch(self):
        return datetime.datetime(1980, 1, 1)


class MacOSXEpoch(Epoch):
    """2001 is the year of the release of Mac OS X 10.0"""
    def epoch(self):
        return datetime.datetime(2001, 1, 1)
