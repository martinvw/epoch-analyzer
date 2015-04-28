import unittest
import datetime

from epoch_analyzer import DateTimeBitPackedScorer

class BitPackedStringMappingTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_two_way_conversion(self):
        input_string = "YYYYYYMM MMDDDDDh hhhhmmmm mmssssss"
        mapping = DateTimeBitPackedScorer.convert_string_to_mapping(input_string)
        output_string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
        self.assertEqual(input_string, output_string)

        input_string = "YYYYYYYM MMMDDDDD hhhhhmmm mmmsssss"
        mapping = DateTimeBitPackedScorer.convert_string_to_mapping(input_string)
        output_string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
        self.assertEqual(input_string, output_string)

        input_string = "MMMMDDDD Dhhhhhmm mmmmssss ss?????? YYYYYYYY"
        mapping = DateTimeBitPackedScorer.convert_string_to_mapping(input_string)
        output_string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
        self.assertEqual(input_string, output_string)

    def test_two_way_conversion_inverse(self):
        mapping = { 'Y': (26, 6),
                    'M': (22, 4),
                    'D': (17, 5),
                    'h': (12, 5),
                    'm': (6, 6),
                    's': (0, 6), }

        string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
        output_mapping = DateTimeBitPackedScorer.convert_string_to_mapping(string)
        self.assertEqual(mapping, output_mapping)

        mapping = { 'Y': (40, 6),
                    'M': (32, 4),
                    'D': (24, 5),
                    'h': (16, 5),
                    'm': (8, 6),
                    's': (0, 6), }

        string = DateTimeBitPackedScorer.convert_mapping_to_string(mapping)
        output_mapping = DateTimeBitPackedScorer.convert_string_to_mapping(string)
        self.assertEqual(mapping, output_mapping)
