import datetime

from .date_time import DateTimeScorer

class DateTimeCompositionScorer(DateTimeScorer):
    def __init__(self, minDate, maxDate, epoch, unit):
        self.epoch = epoch
        self.unit  = unit
        super(DateTimeCompositionScorer, self).__init__(minDate, maxDate)


    def convertToNumber(self, date):
        return (date - self.epoch.epoch()).total_seconds() * self.unit.unit()


    def convertToDate(self, number):
        try:
            secondsSinceEpoch = number / self.unit.unit()
            return self.epoch.epoch() + datetime.timedelta(seconds = secondsSinceEpoch)
        except:
            return -1


    def __str__(self):
        return 'NumberOf' + str(self.unit) + 'Since' + str(self.epoch)
