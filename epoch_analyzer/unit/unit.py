from abc import ABCMeta
from abc import abstractmethod

class Unit(metaclass = ABCMeta):
    @abstractmethod
    def unit(self):
        """ this method should be implemented in one of the childs. """


    def convert_to_seconds(self, number):
        return number / self.unit()


    def __str__(self):
        return type(self).__name__.replace('Unit', '')


class DaysUnit(Unit):
    def unit(self):
        return 1 / (60 * 60 * 24)


class MinutesUnit(Unit):
    def unit(self):
        return 1 / 60


class SecondsUnit(Unit):
    def unit(self):
        return 1


class MiliSecondsUnit(Unit):
    def unit(self):
        return 1000


class MicroSecondsUnit(Unit):
    def unit(self):
        return 1000 * 1000


class TicksUnit(Unit):
    def unit(self):
        return 1000 * 1000 * 10
