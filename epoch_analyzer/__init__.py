# -*- coding: utf-8 -*-
__version__ = '0.1'

import re

from .date_time_composition import *
from .date_time_bitpacked import *
from .epoch import *
from .unit import *
from collections import Counter, OrderedDict, Iterable
import logging

__all__ = ["EpochTester", "DateTimeCompositionScorer", "FATTimestampScorer", "SiemensDVRTimestampScorer"]

class EpochTester(object):
    DEFAULT_MIN_DAYS = 8 * 365
    DEFAULT_MAX_DAYS = 0.5 * 365

    def __init__(self, min_date = None, max_date = None, verbose = False):
        today = datetime.datetime.today()
        if min_date == None: min_date = today - datetime.timedelta(days = self.DEFAULT_MIN_DAYS)
        if max_date == None: max_date = today + datetime.timedelta(days = self.DEFAULT_MAX_DAYS)

        self.min_date = min_date
        self.max_date = max_date
        self.verbose = verbose

        self.__init_testers()

    def test(self, values, return_percentage = False):
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
            if return_percentage: result[value] *= 100

        return result

    def convert(self, values, force_scorer = None):
        if not isinstance(values, Iterable): values = {values}

        result = OrderedDict()

        for value in values:
            result[value] = None
            # iterate all the different test classes
            for name, scorer in self.testClasses.items():
                if force_scorer and force_scorer != name: continue

                score = scorer.score(value)
                if score > 0 or force_scorer == name:
                    if not result[value]: result[value] = ()
                    result[value] += ((name, scorer.convertToDate(value)),)
                    logging.info("{} could be of type {} with actual date {}".format(value, name, scorer.convertToDate(value)))

        return result

    def __init_testers(self):
        units = {TicksUnit(), MicroSecondsUnit(), MiliSecondsUnit(), SecondsUnit(), MinutesUnit(), DaysUnit()}
        epochs = {MacOSXEpoch(), UnixEpoch(), ExcelEpoch(), MacOSEpoch(), NTPEpoch(), MicrosoftEpoch(), DotNetEpoch()}

        first_cap_re = re.compile('(.)([A-Z][a-z]+)')
        all_cap_re = re.compile('([a-z0-9])([A-Z])')

        self.testClasses = {}

        for unit in units:
            unit_name = type(unit).__name__.replace('Unit', '')
            for epoch in epochs:
                epoch_name = type(epoch).__name__
                full_name = 'NumberOf' + unit_name + 'Since' + epoch_name
                full_name = all_cap_re.sub(r'\1 \2', first_cap_re.sub(r'\1 \2',full_name))
                self.testClasses[full_name] = DateTimeCompositionScorer(self.min_date, self.max_date, epoch, unit)

        self.testClasses['FAT timestamp'] = FATTimestampScorer(self.min_date, self.max_date)
        self.testClasses['Siemens DVR timestamp']  = SiemensDVRTimestampScorer(self.min_date, self.max_date)
