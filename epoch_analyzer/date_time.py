from abc import ABCMeta
from abc import abstractmethod

class DateTimeScorer(metaclass = ABCMeta):

    def __init__(self, min_date, max_date, ordered = True):
        self.min_date = min_date
        self.max_date = max_date
        self.ordered = ordered
        self.min_value = self.convert_to_number(self.min_date)
        self.max_value = self.convert_to_number(self.max_date)


    def score(self, number):
        if self.ordered:
            matches = self.min_value < number and self.max_value > number
        else:
            date = self.convert_to_date(number)
            matches = date and self.min_date < date and self.max_date > date

        return 1 if matches else 0


    @abstractmethod
    def convert_to_number(self, date):
        """ this method should be implemented in one of the childs. """


    @abstractmethod
    def convert_to_date(self, number):
        """ this method should be implemented in one of the childs. """
