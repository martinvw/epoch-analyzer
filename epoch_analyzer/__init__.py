# -*- coding: utf-8 -*-
__version__ = '0.1'


from .date_time_composition import *
from .date_time_bitpacked import *
from date_time.epoch import *
from date_time.unit import *
from collections import Counter
import logging

__all__ = ["EpochTester", "DateTimeCompositionScorer", "FATTimestampScorer", "SiemensDVRTimestampScorer"]

class EpochTester(object):
    DEFAULT_MIN_DAYS = 5 * 365
    DEFAULT_MAX_DAYS = 0.5 * 365

    def __init__(self, min_date = None, max_date = None, verbose = False):
        today = datetime.datetime.today()
        if min_date == None: min_date = today - datetime.timedelta(days = DEFAULT_MIN_DAYS)
        if max_date == None: max_date = today + datetime.timedelta(days = DEFAULT_MAX_DAYS)

        self.min_date = min_date
        self.max_date = max_date
        self.verbose = verbose

        self.__init_testers()

    def test(self, values):
        if not isinstance(values, Counter): values = Counter(values)

        result = Counter()
        total_count = 0

        for value, count in values.items():
            total_count += count
            # iterate all the different test classes
            for name, scorer in self.testClasses.items():
                score = scorer.score(value)
                if score > 0:
                    logging.info("{} could be of type {} with actual date {}".format(value, name, scorer.convertToDate(value)))
                    result[name] += score * count

        for value, count in result.items():
            result[value] = count / total_count

        return result

    def convert(self, values):
        if not isinstance(values, Counter): values = Counter(values)

        for value, count in values.items():
            # iterate all the different test classes
            for name, scorer in self.testClasses.items():
                score = scorer.score(value)
                if score > 0:
                    print("{} could be of type {} with actual date {}".format(value, name, scorer.convertToDate(value)))

    def __init_testers(self):
        units = {TicksUnit(), MicroSecondsUnit(), MiliSecondsUnit(), SecondsUnit(), MinutesUnit(), DaysUnit()}
        epochs = {MacOSXEpoch(), UnixEpoch(), ExcelEpoch(), MacOSEpoch(), NTPEpoch(), MicrosoftEpoch(), DotNetEpoch()}

        self.testClasses = {}

        for unit in units:
            unit_name = type(unit).__name__.replace('Unit', '')
            for epoch in epochs:
                epoch_name = type(epoch).__name__
                full_name = unit_name + 'Since' + epoch_name
                self.testClasses[full_name] = DateTimeCompositionScorer(self.min_date, self.max_date, epoch, unit)

        self.testClasses['FATTimestamp'] = FATTimestampScorer(self.min_date, self.max_date)
        self.testClasses['SiemensDVRTimestamp']  = SiemensDVRTimestampScorer(self.min_date, self.max_date)
