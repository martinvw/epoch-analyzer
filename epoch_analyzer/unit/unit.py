from abc import ABCMeta
from abc import abstractmethod
from ..epoch import *

class Unit(metaclass = ABCMeta):
    @abstractmethod
    def unit(self):
        """ this method should be implemented in one of the childs. """

    """Calculate the weight given the unit"""
    def weight(self, epoch):
        return 1


    def convert_to_seconds(self, number):
        return number / self.unit()


    def __str__(self):
        return type(self).__name__.replace('Unit', '')


class DaysUnit(Unit):
    def unit(self):
        return 1 / (60 * 60 * 24)


    def weight(self, epoch):
        instance = isinstance(epoch, ExcelEpoch)
        return .5 if instance else .01


class MinutesUnit(Unit):
    def unit(self):
        return 1 / 60


    def weight(self, epoch):
        return .1


class SecondsUnit(Unit):
    def unit(self):
        return 1


class MiliSecondsUnit(Unit):
    def unit(self):
        return 1000


    def weight(self, epoch):
        instance = isinstance(epoch, UnixEpoch)
        return .8 if instance else .5


class MicroSecondsUnit(Unit):
    def unit(self):
        return 1000 * 1000


    def weight(self, epoch):
        instance = isinstance(epoch, MicrosoftEpoch) or isinstance(epoch, UnixEpoch)
        return .8 if instance else .5


class TicksUnit(Unit):
    def unit(self):
        return 1000 * 1000 * 10


    def weight(self, epoch):
        instance = isinstance(epoch, MicrosoftEpoch)
        return .8 if instance else .1
