import datetime
import math
import operator
import re
import logging

from collections import OrderedDict

from .date_time import DateTimeScorer


class DateTimeBitPackedScorer(DateTimeScorer):
    def __init__(self, minDate, maxDate, mapping = None, date_format_string = None, ordered = True):
        if date_format_string:
            self.mapping = DateTimeBitPackedScorer.convert_string_to_mapping(date_format_string)
        elif mapping:
            self.mapping = mapping
        else:
            raise Exception("Illegal argument, either date_format_string or prepaired mapping")
        super(DateTimeBitPackedScorer, self).__init__(minDate, maxDate, ordered)

    def convert_to_date(self, number):
        # bit magic only works with integers
        number = int(number)
        try:
            day    = self.day_transformation     ((number >> self.bitshift('D')) & self.mask('D'))
            month  = self.month_transformation   ((number >> self.bitshift('M')) & self.mask('M'))
            year   = self.year_transformation    ((number >> self.bitshift('Y')) & self.mask('Y'))
            second = self.second_transformation  ((number >> self.bitshift('s')) & self.mask('s'))
            minute = self.minute_transformation  ((number >> self.bitshift('m')) & self.mask('m'))
            hour   = self.hour_transformation    ((number >> self.bitshift('h')) & self.mask('h'))
            return datetime.datetime(year, month, day, hour, minute, second)
        except ValueError:
            # eg. ValueError: month must be in 1..12
            return
        except Exception as err:
            logging.warning(err)
            return

    def bitshift(self, type):
        return self.mapping[type][0]

    def mask(self, type):
        return (1 << self.mapping[type][1]) - 1

    def convert_to_number(self, date):
        result =  self.second_transformation(date.second, reverse=True) << self.mapping['s'][0]
        result += self.minute_transformation(date.minute, reverse=True) << self.mapping['m'][0]
        result += self.hour_transformation(date.hour, reverse=True)     << self.mapping['h'][0]
        result += self.day_transformation(date.day, reverse=True)       << self.mapping['D'][0]
        result += self.month_transformation(date.month, reverse=True)   << self.mapping['M'][0]
        result += self.year_transformation(date.year, reverse=True)     << self.mapping['Y'][0]
        return result

    def __str__(self):
        return "BitMask " + self.convert_mapping_to_string(self.mapping)

    @staticmethod
    def convert_mapping_to_string(mapping):
        max_value = 0
        values = {}
        result = ''

        # determine maximum and collection positions and string (lengths)
        for k, v in mapping.items():
            max_value = max(max_value, v[0] + v[1])
            values[v[0]+v[1]] = (k * v[1])

        # sort dict by keys
        values = OrderedDict(sorted(values.items(), reverse=True))
        # reconstruct the string
        i = math.ceil(max_value / 8) * 8
        while i > 0:
            addition = values[i] if i in values else '?'
            result += addition
            i -= len(addition)

        # add whitespace in between bytes
        return re.sub('([DMYsmh\?]{8})', r'\g<1> ', result).strip()

    @staticmethod
    def convert_string_to_mapping(string):
        # trim any whitespace in between
        string = string.replace(' ', '')

        mapping = {}
        previous = None
        count = 0
        position = len(string)
        for c in string[::-1]:
            if previous == None: previous = c

            # is this a different char than we were processing
            if previous != c:
                mapping[previous] = (len(string)-position, count, )
                position = position - count
                count = 1
                previous = c
            else:
                count += 1

        # add the remaining data
        mapping[previous] = (len(string)-position, count, )

        # leave out the ? in the mappings
        if '?' in mapping: del mapping['?']

        return mapping

    def year_transformation(self, value, reverse=False):
        return value

    def month_transformation(self, value, reverse=False):
        return value

    def day_transformation(self, value, reverse=False):
        return value

    def hour_transformation(self, value, reverse=False):
        return value

    def minute_transformation(self, value, reverse=False):
        return value

    def second_transformation(self, value, reverse=False):
        return value

    def plus(self, a, b, reverse=False):
       return operator.add(a, b) if not reverse else operator.sub(a, b)

    def mul(self, a, b, reverse=False):
       return operator.mul(a, b) if not reverse else operator.truediv(a,b)

class FATTimestampScorer(DateTimeBitPackedScorer):
    def __init__(self, minDate, maxDate):
        format_string = "YYYYYYYM MMMDDDDD hhhhhmmm mmmsssss"
        super(FATTimestampScorer, self).__init__(minDate, maxDate, date_format_string=format_string)

    def year_transformation(self, value, reverse=False):
        return self.plus(value, 1980, reverse)

    def second_transformation(self, value, reverse=False):
        return int(self.mul(value, 2, reverse))


class FourByteBitTimestampScorer(DateTimeBitPackedScorer):
    def __init__(self, minDate, maxDate):
        format_string = 'YYYYYYMM MMDDDDDh hhhhmmmm mmssssss'
        super(FourByteBitTimestampScorer, self).__init__(minDate, maxDate, date_format_string=format_string)

    def year_transformation(self, value, reverse=False):
        return self.plus(value, 1970, reverse)

class FourByteBitTimestampScorer2000(FourByteBitTimestampScorer):
    def __init__(self, minDate, maxDate):
        super(FourByteBitTimestampScorer2000, self).__init__(minDate, maxDate)

    def year_transformation(self, value, reverse=False):
        return self.plus(value, 2000, reverse)


class FiveByteBitTimestampScorer(DateTimeBitPackedScorer):
    def __init__(self, minDate, maxDate):
        format_string = 'MMMMDDDD Dhhhhhmm mmmmssss ss?????? YYYYYYYY'
        super(FiveByteBitTimestampScorer, self).__init__(minDate, maxDate, date_format_string=format_string, ordered=False)

    def year_transformation(self, value, reverse=False):
        return self.plus(value, 2000, reverse)
