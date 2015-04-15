from abc import ABCMeta
from abc import abstractmethod

class DateTimeScorer(metaclass = ABCMeta):

    def __init__(self, minDate, maxDate, ordered = True):
        self.minDate = minDate
        self.maxDate = maxDate
        self.ordered = ordered
        self.minValue = self.convertToNumber(self.minDate)
        self.maxValue = self.convertToNumber(self.maxDate)


    def score(self, number):
        if self.ordered:
            matches = self.minValue < number and self.maxValue > number
        else:
            date = self.convertToDate(number)
            matches = date and self.minDate < date and self.maxDate > date

        return 1 if matches else 0


    @abstractmethod
    def convertToNumber(self, date):
        return


    @abstractmethod
    def convertToDate(self, number):
        return
