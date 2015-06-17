import unittest
import datetime

from epoch_analyzer import EpochTester

class EpochTesterConvertTest(unittest.TestCase):
    def setUp(self):
        self.tester = EpochTester(datetime.datetime(2014,1,1), datetime.datetime(2015,1,1))
        self.reference_date = datetime.datetime(2014,11,5,19,52,34)

    def test_single_fat(self):
        value_numeric = 1164287633
        value = self.tester.convert(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get(value_numeric)[0][0], 'FAT timestamp')
        self.assertEqual(value.get(value_numeric)[0][1], self.reference_date)

    def test_single_4byte(self):
        value_numeric = 2999663906
        value = self.tester.convert(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get(value_numeric)[0][0], '4-Bytes bit-based timestamp since 1970')
        self.assertEqual(value.get(value_numeric)[0][1], self.reference_date)

    def test_single_5byte(self):
        value_numeric = 767981813774
        value = self.tester.convert(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get(value_numeric)[0][0], '5-Bytes bit-based timestamp')
        self.assertEqual(value.get(value_numeric)[0][1], self.reference_date)

    def test_multi(self):
        values_numeric = (1164287633,1164287633,1164287633, 2999663906, 767981813774,)
        value = self.tester.convert(values_numeric)

        # returns only unique results
        self.assertEqual(len(value),  3)

        self.assertEqual(value.get(1164287633)[0][0], 'FAT timestamp')
        self.assertEqual(value.get(1164287633)[0][1], self.reference_date)

        self.assertEqual(value.get(2999663906)[0][0], '4-Bytes bit-based timestamp since 1970')
        self.assertEqual(value.get(2999663906)[0][1], self.reference_date)

        self.assertEqual(value.get(767981813774)[0][0], '5-Bytes bit-based timestamp')
        self.assertEqual(value.get(767981813774)[0][1], self.reference_date)
