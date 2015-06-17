# -*- coding: utf-8 -*-
__version__ = '0.3'

import re
import datetime

from .date_time_composition import *
from .date_time_bitpacked import *
from .epoch import *
from .unit import *
from collections import Counter, OrderedDict, Iterable
import logging

__all__ = ["EpochTester", "DateTimeCompositionScorer", "FATTimestampScorer", "FourByteBitTimestampScorer", "FourByteBitTimestampScorer2000", "FiveByteBitTimestampScorer"]

class EpochTester(object):
    DEFAULT_MIN_DAYS = 9 * 365
    DEFAULT_MAX_DAYS = 0.5 * 365

    def __init__(self, min_date = None, max_date = None):
        today = datetime.datetime.today()
        if min_date == None: min_date = today - datetime.timedelta(days = self.DEFAULT_MIN_DAYS)
        if max_date == None: max_date = today + datetime.timedelta(days = self.DEFAULT_MAX_DAYS)

        if isinstance(min_date, datetime.date):  min_date = datetime.datetime.combine(min_date, datetime.datetime.min.time())
        if isinstance(max_date, datetime.date):  max_date = datetime.datetime.combine(max_date, datetime.datetime.min.time())

        self.min_date = min_date
        self.max_date = max_date

        self.__init_testers()


    def test(self, values, return_percentage = False):
        if not isinstance(values, Iterable): values = {values}
        if not isinstance(values, Counter): values = Counter(values)

        result = Counter()
        total_count = 0

        for value, count in values.items():
            total_count += count
            # iterate all the different test classes
            for name, scorer in self.__test_classes.items():
                score = scorer.score(value)
                if score > 0:
                    logging.info("{} could be of type {} with actual date {}".format(value, name, scorer.convert_to_date(value)))
                    result[name] += score * count

        for value, count in result.items():
            result[value] = count / total_count
            if return_percentage: result[value] *= 100

        return result


    def convert(self, values, force_scorer = None):
        if not isinstance(values, Iterable): values = {values}

        result = OrderedDict()

        for value in values:
            result[value] = None
            # iterate all the different test classes
            for name, scorer in self.__test_classes.items():
                if force_scorer and force_scorer != name: continue

                score = scorer.score(value)
                if score > 0 or force_scorer == name:
                    if not result[value]: result[value] = ()
                    result[value] += ((name, scorer.convert_to_date(value)),)
                    logging.info("{} could be of type {} with actual date {}".format(value, name, scorer.convert_to_date(value)))

        return result


    def get_convertor(self, requested_label):
        # magic number 5, is indeed arbitrary chosen
        if len(requested_label) < 5: return

        if requested_label in self.__test_classes:
            return self.__test_classes[requested_label]

        requested_label = requested_label.lower()

        for label, scorer in self.__test_classes.items():
            if label.lower().startswith(requested_label):
                return scorer


    def get_available_testers(self):
        return self.__test_classes.keys()


    def register_test_class(self, name, timestamp_class):
        self.__test_classes[name] = timestamp_class(self.min_date, self.max_date)


    def __init_testers(self):
        units = {TicksUnit(), MicroSecondsUnit(), MiliSecondsUnit(), SecondsUnit(), MinutesUnit(), DaysUnit()}
        epochs = {MacOSXEpoch(), UnixEpoch(), ExcelEpoch(), MacOSEpoch(), NTPEpoch(), MicrosoftEpoch(), DotNetEpoch(), FATEpoch()}

        first_cap_re = re.compile('(.)([A-Z][a-z]+)')
        all_cap_re = re.compile('([a-z0-9])([A-Z])')

        self.__test_classes = {}

        for unit in units:
            for epoch in epochs:
                scorer = DateTimeCompositionScorer(self.min_date, self.max_date, epoch, unit)
                full_name = all_cap_re.sub(r'\1 \2', first_cap_re.sub(r'\1 \2',str(scorer)))
                self.__test_classes[full_name] = scorer

        self.__test_classes['FAT timestamp'] = FATTimestampScorer(self.min_date, self.max_date)
        self.__test_classes['4-Bytes bit-based timestamp since 1970']  = FourByteBitTimestampScorer(self.min_date, self.max_date)
        self.__test_classes['4-Bytes bit-based timestamp since 2000']  = FourByteBitTimestampScorer2000(self.min_date, self.max_date)
        self.__test_classes['5-Bytes bit-based timestamp']  = FiveByteBitTimestampScorer(self.min_date, self.max_date)
