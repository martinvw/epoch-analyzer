import datetime

from .date_time import DateTimeScorer

class DateTimeCompositionScorer(DateTimeScorer):
    def __init__(self, minDate, maxDate, epoch, unit):
        self.epoch = epoch
        self.unit  = unit
        super(DateTimeCompositionScorer, self).__init__(minDate, maxDate)

    def convert_to_number(self, date):
        return (date - self.epoch.epoch()).total_seconds() * self.unit.unit()

    def convert_to_date(self, number):
        try:
            secondsSinceEpoch = self.unit.convert_to_seconds(number)
            return self.epoch.epoch() + datetime.timedelta(seconds = secondsSinceEpoch)
        except:
            return -1


    def __str__(self):
        return 'NumberOf' + str(self.unit) + 'Since' + str(self.epoch)
