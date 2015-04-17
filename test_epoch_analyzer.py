import datetime

from epoch_analyzer import EpochTester
from epoch_analyzer.date_time_bitpacked import *

today = datetime.datetime.today()
min_date = today - datetime.timedelta(days = 4 * 365)
max_date = today + datetime.timedelta(days = 0.5 * 365)

tester = EpochTester(min_date, max_date)
result = tester.convert((1164287633,1164287633,1164287633, 2999663906, 767981813774,))
print(result)

<<<<<<< HEAD
tester = EpochTester(min_date, max_date)
result = tester.test((1164287633,1164287633,1164287633, 2999663906, 767981813774,))
=======
tester = EpochTester()
result = tester.test((962961041, 2597010722, 767981813768,))
>>>>>>> 9bac70131b743e0d6168d1bf5ff366e62cb18e79
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
print(inputString, ' != ', string)

date_time = datetime.datetime(2014, 11, 5, 19, 52, 34)
scorer = SiemensDVRTimestampScorer(min_date, max_date)
print("SiemensDVRTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 2999663906)
print(scorer.convertToDate(result), " =? ", date_time)

scorer = FATTimestampScorer(min_date, max_date)
print("FATTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 1164287633)
print(scorer.convertToDate(result), " =? ", date_time)

scorer = FiveByteBitTimestampScorer(min_date, max_date)
print("FiveByteBitTimestampScorer => ", str(scorer))
result = scorer.convertToNumber(date_time)
print(result, " =? ", 767981813774)
print(scorer.convertToDate(result), " =? ", date_time)

for name, scorer in tester.testClasses.items():
    result = scorer.convertToNumber(date_time)
    print(str(scorer),": (",result,")", scorer.convertToDate(result), " =? ", date_time)
