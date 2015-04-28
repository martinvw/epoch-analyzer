import unittest
import datetime

from epoch_analyzer import EpochTester

class ConvertorTest(unittest.TestCase):
    def setUp(self):
        self.tester = EpochTester(datetime.datetime(2014,1,1), datetime.datetime(2015,1,1))
        self.reference_date = datetime.datetime(2014,11,5,19,40,48)

    def test_four_bytes_bit_bases(self):
        scorer = self.tester.get_convertor('4-Bytes bit-based timestamp')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 2999663152)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_fat_timestamp(self):
        scorer = self.tester.get_convertor('FAT timestamp')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 1164287256)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_five_bytes_bit_bases(self):
        scorer = self.tester.get_convertor('5-Bytes bit-based timestamp')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 767969460238)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_unix_time(self):
        scorer = self.tester.get_convertor('Number Of Seconds Since Unix Epoch')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 1415216448)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_miliseconds_since_dot_net(self):
        scorer = self.tester.get_convertor('Number Of Mili Seconds Since Dot Net Epoch')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 63550813248000)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_ms_excel_time(self):
        scorer = self.tester.get_convertor('Number Of Days Since Excel Epoch')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 41948.82)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)

    def test_osx_time(self):
        scorer = self.tester.get_convertor('Number Of Mili Seconds Since Mac OSX Epoch')
        result = scorer.convert_to_number(self.reference_date)
        self.assertEqual(result, 436909248000)
        self.assertEqual(scorer.convert_to_date(result), self.reference_date)
