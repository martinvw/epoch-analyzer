from abc import ABCMeta
from abc import abstractmethod

class DateTimeScorer(metaclass = ABCMeta):

    def __init__(self, minDate, maxDate):
        self.minDate = minDate
        self.maxDate = maxDate


    @abstractmethod
    def score(self, number):
        return


    @abstractmethod
    def convertToNumber(self, date):
        return


    @abstractmethod
    def convertToDate(self, number):
        return


class OrderedDateTimeScorer(DateTimeScorer):
    def __init__(self, minDate, maxDate):
        super(OrderedDateTimeScorer, self).__init__(minDate, maxDate)
        self.initialize()


    def initialize(self):
        self.minValue = self.convertToNumber(self.minDate)
        self.maxValue = self.convertToNumber(self.maxDate)


    def score(self, number):
        if self.minValue < number and self.maxValue > number:
            return 1
        else:
            return 0
