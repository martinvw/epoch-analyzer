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

def main():
    parser = argparse.ArgumentParser(description='Analyse for possible datetime values.')
    parser.add_argument('--min', help='supply the minimum date for analysis', type=valid_date)
    parser.add_argument('--max', help='supply the maximum date for analysis', type=valid_date)
    parser.add_argument('--summary', '-s', action='store_true', help='show summary instead of individual conversions.')
    parser.add_argument('--table_width','-t', metavar='<N>', help='Supply the table width for analysis', required = True, type=int)
    # ? offset / length

    parser.add_argument('file', help='supply the file to analyze', type=argparse.FileType('rb'))

    args = parser.parse_args()


    tester = EpochTester(args.min, args.max)
    searcher = EpochSearcher(tester, args.file, args.table_width)
    searcher.process();

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

class EpochSearcher(object):
    def __init__(self, tester, file, table_width):
        self.tester = tester
        self.file = file
        self.table_width = table_width


    def process(self):
        result = self.file.read(1024)
        matches = {}

        for start in range(len(result)):
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


                        #matches.append(value)
                        #print(test_result)
                        #print("Trying length %d, at pos %d: %d" % (byte_size, start, value))
                        #print("Relative pos: %d" % relative_pos)

        row = random.randint(0, (len(result) / self.table_width))
        start_position = row * self.table_width
        self.file.seek(start_position, 0)
        block = self.file.read(self.table_width)
        hex_string = binascii.b2a_hex(block).upper().decode('utf-8')

        example_results = {}

        for key, sub_matches in matches.items():
             parts = key.split(':')
             start_pos = int(parts[0])
             byte_size = int(parts[1])
             signed = parts[2]
             byte_order = parts[3]
             results = self.tester.test(sub_matches, byte_size=byte_size).most_common(5)
             for label, score in results:
                if score > 0.7:

                    value = int.from_bytes(block[start_pos:start_pos + byte_size], byteorder = byte_order, signed = signed)
                    result = self.tester.get_convertor(label).convert_to_date(value)
                    string = ""

                    for i, c in enumerate(hex_string):
                        position = (i / 2)
                        if position > 0 and position % 4 == 0: string += ' '
                        if position >= start_pos and position < start_pos + byte_size:
                            string += colored(c, 'green', attrs=['reverse'])
                        else:
                            string += c

                    string += "\t(%s end.)\t%d \t=>   %s %s [%f]" % (byte_order, value, str(result).ljust(22, ' '), label, score)
                    example_results[key + label] = string

        print("Sample picked from offset: %d" % start_position)

        for key in sorted(example_results):
            print(example_results[key])


if __name__ == '__main__':
    main()
