import datetime

from date_time.date_time import OrderedDateTimeScorer


class DateTimeBitPackedScorer(OrderedDateTimeScorer):
    def __init__(self, minDate, maxDate, mapping):
        self.mapping = mapping
        super(DateTimeBitPackedScorer, self).__init__(minDate, maxDate)

    def convertToDate(self, number):
        try:
            day     = self.dayTransformation     ((number >> self.bitshift('day')) & self.mask('day'))
            month   = self.monthTransformation   ((number >> self.bitshift('month')) & self.mask('month'))
            year    = self.yearTransformation    ((number >> self.bitshift('year')) & self.mask('year'))
            second = self.secondTransformation  ((number >> self.bitshift('second')) & self.mask('second'))
            minute = self.minuteTransformation  ((number >> self.bitshift('minute')) & self.mask('minute'))
            hour   = self.hourTransformation    ((number >> self.bitshift('hour')) & self.mask('hour'))

            return datetime.datetime(year, month, day, hour, minute, second)
        except:
            return

    def bitshift(self, type):
        return self.mapping[type][0]

    def mask(self, type):
        return (1 << self.mapping[type][1]) - 1

    def convertToNumber(self, date):
        result =  self.reverseSecondTransformation(date.second) << self.mapping['second'][0]
        result += self.reverseMinuteTransformation(date.minute) << self.mapping['minute'][0]
        result += self.reverseHourTransformation(date.hour)     << self.mapping['hour'][0]
        result += self.reverseDayTransformation(date.day)       << self.mapping['day'][0]
        result += self.reverseMonthTransformation(date.month)   << self.mapping['month'][0]
        result += self.reverseYearTransformation(date.year)     << self.mapping['year'][0]
        return result

    def reverseYearTransformation(self, value):
        return value

    def yearTransformation(self, value):
        return value

    def reverseMonthTransformation(self, value):
        return value

    def monthTransformation(self, value):
        return value

    def reverseDayTransformation(self, value):
        return value

    def dayTransformation(self, value):
        return value

    def reverseHourTransformation(self, value):
        return value

    def hourTransformation(self, value):
        return value

    def reverseMinuteTransformation(self, value):
        return value

    def minuteTransformation(self, value):
        return value

    def reverseSecondTransformation(self, value):
        return value

    def secondTransformation(self, value):
        return value


class FATTimestampScorer(DateTimeBitPackedScorer):
    def __init__(self, minDate, maxDate):
        mapping = {}
        mapping['second']  = [0, 5]
        mapping['minute']  = [5, 6]
        mapping['hour']    = [11,5]
        mapping['day']     = [16,5]
        mapping['month']   = [21,4]
        mapping['year']    = [25,7]
        super(FATTimestampScorer, self).__init__(minDate, maxDate, mapping)

    def reverseYearTransformation(self, value):
        return value - 1980

    def yearTransformation(self, value):
        return value + 1980

    def reverseSecondTransformation(self, value):
        return int(value / 2)

    def secondTransformation(self, value):
        return value * 2


class SiemensDVRTimestampScorer(DateTimeBitPackedScorer):
    def __init__(self, minDate, maxDate):
        mapping = {}
        mapping['second']  = [0, 6]
        mapping['minute']  = [6, 6]
        mapping['hour']    = [12,5]
        mapping['day']     = [17,5]
        mapping['month']   = [22,4]
        mapping['year']    = [26,6]
        super(SiemensDVRTimestampScorer, self).__init__(minDate, maxDate, mapping)

    def reverseYearTransformation(self, value):
        return value - 1970

    def yearTransformation(self, value):
        return value + 1970
