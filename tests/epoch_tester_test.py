import unittest
import datetime

from epoch_analyzer import EpochTester

class EpochTesterTestTest(unittest.TestCase):
    def setUp(self):
        self.tester = EpochTester(datetime.datetime(2014,1,1), datetime.datetime(2015,1,1))
        self.reference_date = datetime.datetime(2014,11,5,19,52,34)

    def test_single_fat(self):
        value_numeric = 1164287633
        value = self.tester.test(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get('FAT timestamp'), 1.0)


    def test_single_4byte(self):
        value_numeric = 2999663906
        value = self.tester.test(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get('4-Bytes bit-based timestamp since 1970'), 1.0)


    def test_single_5byte(self):
        value_numeric = 767981813774
        value = self.tester.test(value_numeric)
        self.assertEqual(len(value),  1)
        self.assertEqual(value.get('5-Bytes bit-based timestamp'), 1.0)


    def test_multi(self):
        values_numeric = (1164287633,1164287633,1164287633, 2999663906, 767981813774,)
        value = self.tester.test(values_numeric)
        self.assertEqual(len(value),  3)
        self.assertEqual(value.get('FAT timestamp'), 0.6)
        self.assertEqual(value.get('4-Bytes bit-based timestamp since 1970'), 0.2)
        self.assertEqual(value.get('5-Bytes bit-based timestamp'), 0.2)
