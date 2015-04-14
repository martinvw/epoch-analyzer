from epoch_analyzer import EpochTester
from epoch_analyzer.date_time_bitpacked import DateTimeBitPackedScorer

tester = EpochTester()
result = tester.convert((2660317541,2443065701,962961041,))
print(result)

for k,v in tester.testClasses.items():
    print("{} => {}".format(k, v))

print(DateTimeBitPackedScorer.convertStringToMapping("YYYYYYMM MMDDDDDh hhhhmmmm mmssssss"))
