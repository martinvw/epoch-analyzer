import datetime

from epoch_analyzer import EpochTester
from epoch_analyzer.date_time_bitpacked import *

today = datetime.datetime.today()
min_date = today - datetime.timedelta(days = 4 * 365)
max_date = today + datetime.timedelta(days = 0.5 * 365)

values = (1164287633,1164287633,1164287633, 2999663906, 767981813774,)

tester = EpochTester(min_date, max_date)
result = tester.convert(values)
print(result)

tester = EpochTester(min_date, max_date)
result = tester.test(values)
print(result)

inputString = "YYYYYYMM MMDDDDDh hhhhmmmm mmssssss"
mapping = DateTimeBitPackedScorer.convert_string_to_mapping(inputString)
string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
print(inputString, ' =? ', string)

inputString = "YYYYYYYM MMMDDDDD hhhhhmmm mmmsssss"
mapping = DateTimeBitPackedScorer.convert_string_to_mapping(inputString)
string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
print(inputString, ' =? ', string)

inputString = "MMMMDDDD Dhhhhhmm mmmmssss ss?????? YYYYYYYY"
mapping = DateTimeBitPackedScorer.convert_string_to_mapping(inputString)
string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
print(inputString, ' =? ', string)

inputString = "MMMMDDDD Dhhhhhmm mmmmssss ss"
mapping = DateTimeBitPackedScorer.convert_string_to_mapping(inputString)
string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
print(inputString, ' =? ', string)

date_time = datetime.datetime(2014, 11, 5, 19, 52, 34)
scorer = tester.get_convertor('4-Bytes bit-based timestamp')
print("4-Bytes bit-based timestamp => ", str(scorer))
result = scorer.convert_to_number(date_time)
print(result, " =? ", 2999663906)
print(scorer.convert_to_date(result), " =? ", date_time)

scorer = tester.get_convertor('FAT timestamp')
print("FAT timestamp => ", str(scorer))
result = scorer.convert_to_number(date_time)
print(result, " =? ", 1164287633)
print(scorer.convert_to_date(result), " =? ", date_time)

scorer = tester.get_convertor('5-Bytes bit-based timestamp')
print("5-Bytes bit-based timestamp => ", str(scorer))
result = scorer.convert_to_number(date_time)
print(result, " =? ", 767981813774)
print(scorer.convert_to_date(result), " =? ", date_time)

for name, scorer in tester._EpochTester__test_classes.items():
    result = scorer.convert_to_number(date_time)
    print(str(scorer),": (",result,")", scorer.convert_to_date(result), " =? ", date_time)
