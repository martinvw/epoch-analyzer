#!/usr/bin/env python3
import argparse
import binascii
import calendar
import datetime
import random
import re
import struct
import sys

from epoch_analyzer import EpochTester
from termcolor import colored

DEFAULT_ROW_COUNT = 100
SCORE_LIMIT = 0.7

def main():
    parser = get_parser()
    args = parser.parse_args()

    tester = EpochTester(args.min, args.max)
    searcher = EpochSearcher(tester, args.file, args.table_width, args.sample, args.count)
    searcher.process();

def get_parser():
    parser = argparse.ArgumentParser(description='Analyse for possible datetime values.')
    parser.add_argument('--min', help='supply the minimum date for analysis', type=valid_date)
    parser.add_argument('--max', help='supply the maximum date for analysis', type=valid_date)
    parser.add_argument('--sample', '-s', help='show a certain sample instead of a random one.', type=int, default=-1)
    parser.add_argument('--count', '-c', help='Process a certain amount of rows instead of the default (%d).' % DEFAULT_ROW_COUNT, type=int, default=DEFAULT_ROW_COUNT)
    parser.add_argument('--table_width','-t', metavar='<N>', help='Supply the table width for analysis', required = True, type=int)
    parser.add_argument('file', help='supply the file to analyze', type=argparse.FileType('rb'))
    return parser

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

class EpochSearcher(object):
    def __init__(self, tester, file, table_width, sample, count):
        self.tester = tester
        self.file = file
        self.table_width = table_width
        self.row_number = sample
        self.count = count

    def get_row_in_hex(self):
        if self.row_number < 0:
            self.row_number = random.randint(0, self.count)

        start_position = self.row_number * self.table_width
        self.file.seek(start_position, 0)
        block = self.file.read(self.table_width)
        hex_string = binascii.b2a_hex(block).upper().decode('utf-8')
        return (block, hex_string)

    def process(self):
        buffer_size = self.count * self.table_width
        result = self.file.read(buffer_size)
        matches = {}

        actual_size = len(result)

	# correct the count if needed
        if (actual_size < buffer_size):
            self.count = actual_size // self.table_width

        for start in range(actual_size):
            for byte_size in range(1, 17):
                for signed in [True, False]:
                    for byte_order in ['little', 'big']:
                        if byte_size == 1 and byte_order == 'big': continue

                        # perform the actual conversion
                        value = int.from_bytes(result[start:start + byte_size], byteorder = byte_order, signed = signed)

                        if signed and value > 0: continue

                        relative_pos = start % self.table_width

                        key = "%03d:%d:%s:%s" % (relative_pos, byte_size, signed, byte_order)

                        if not key in matches: matches[key] = []
                        matches[key].append(value);


        (block, hex_string) = self.get_row_in_hex()

        print("Sample picked from offset: %d" % self.row_number)

        for key, sub_matches in sorted(matches.items()):
             (match_pos, byte_size, signed, byte_order) = key.split(':')
             byte_size = int(byte_size)
             match_pos = int(match_pos)
             results = self.tester.test(sub_matches, byte_size=byte_size).most_common(5)
             for label, score in results:
                if score > SCORE_LIMIT:

                    value = int.from_bytes(block[match_pos:match_pos + byte_size], byteorder = byte_order, signed = signed)
                    result = self.tester.get_convertor(label).convert_to_date(value)

                    if not self.score_valid_overflows(sub_matches): break

                    self.pretty_print_result(hex_string, value, result, match_pos, byte_order, byte_size, label, score)

    def pretty_print_result(self, hex_string, value, result, match_pos, byte_order, byte_size, label, score):
        string = ""
        color = 'green' if byte_order == 'little' else 'blue'

        for i, c in enumerate(hex_string):
            position = (i / 2)
            if position > 0 and position % 4 == 0: string += ' '
            if position >= match_pos and position < match_pos + byte_size:
                string += colored(c, color, attrs=['reverse'])
            else:
                string += c

        print(string, "\t(%s end.)\t%d \t=>   %s %s [%f]" % (byte_order, value, str(result).ljust(22, ' '), label, score))

    def score_valid_overflows(self, numbers):
        previous_value = None
        positive = negative = 0

        score = 0
        for value in numbers:
            if previous_value == None:
                previous_value = value
                continue

            step = value - previous_value
            #print("step: %d" % step)

            if step > 0: positive += 1
            elif step < 0: negative += 1

            if step == 1: score += 10
            elif step > 0 and step < 50: score += 1
            elif step == 256: score -= 50     # 2^8 = 256
            elif step == 65536: score -= 50   # 2^16 = 65536
            elif step == 16777216: score -= 50# 2^16 = 16777216
            elif abs(step) > 16777216: score -= 5

            previous_value = value

        # it should not run two ways
        if positive > (self.count / 8) and negative > (self.count / 8):
            score -= 50

        #print("Overflow score: %d" % score)
        return score >= 0



if __name__ == '__main__':
    main()
