import datetime

from epoch_analyzer import EpochTester
from epoch_analyzer.date_time_bitpacked import *

today = datetime.datetime.today()
min_date = today - datetime.timedelta(days = 9 * 365)
max_date = today + datetime.timedelta(days = 0.5 * 365)

tester = EpochTester()
result = tester.convert((962961041, 2597010722, 767981813768,))
print(result)

tester = EpochTester()
result = tester.test((962961041, 2597010722, 767981813768,))
print(result)

inputString = "YYYYYYMM MMDDDDDh hhhhmmmm mmssssss"
mapping = DateTimeBitPackedScorer.convertStringToMapping(inputString)
string = DateTimeBitPackedScorer.convertMappingToString(mapping)
print(inputString, ' =? ', string)

inputString = "YYYYYYYM MMMDDDDD hhhhhmmm mmmsssss"
mapping = DateTimeBitPackedScorer.convertStringToMapping(inputString)
string = DateTimeBitPackedScorer.convertMappingToString(mapping)
print(inputString, ' =? ', string)

inputString = "MMMMDDDD Dhhhhhmm mmmmssss ss?????? YYYYYYYY"
mapping = DateTimeBitPackedScorer.convertStringToMapping(inputString)
string = DateTimeBitPackedScorer.convertMappingToString(mapping)
print(inputString, ' =? ', string)

inputString = "MMMMDDDD Dhhhhhmm mmmmssss ss"
mapping = DateTimeBitPackedScorer.convertStringToMapping(inputString)
string = DateTimeBitPackedScorer.convertMappingToString(mapping)
print(inputString, ' =? ', string)

date_time = datetime.datetime(2008, 11, 5, 19, 52, 34)
scorer = SiemensDVRTimestampScorer(min_date, max_date)
print("SiemensDVRTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 2597010722)
print(scorer.convertToDate(result), " =? ", date_time)

scorer = FATTimestampScorer(min_date, max_date)
print("FATTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 962961041)
print(scorer.convertToDate(result), " =? ", date_time)

scorer = FiveByteBitTimestampScorer(min_date, max_date)
print("FiveByteBitTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 767981813768)
print(scorer.convertToDate(result), " =? ", date_time)
