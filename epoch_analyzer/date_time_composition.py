import datetime

from .date_time import OrderedDateTimeScorer

class DateTimeCompositionScorer(OrderedDateTimeScorer):
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
