#!/usr/bin/env python3
import argparse
import binascii
import calendar
import datetime
import re
import struct
import sys

from epoch_analyzer import EpochTester

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

                        key = "%d:%d:%s:%s" % (relative_pos, byte_size, signed, byte_order)

                        if not key in matches: matches[key] = []
                        matches[key].append(value);


                        #matches.append(value)
                        #print(test_result)
                        #print("Trying length %d, at pos %d: %d" % (byte_size, start, value))
                        #print("Relative pos: %d" % relative_pos)

        print(matches['4:4:False:little'])
        for key, sub_matches in matches.items():
            byte_size = int(key.split(':')[1])
            results = self.tester.test(sub_matches, byte_size=byte_size).most_common(5)
            for label, score in results:
                if score > 0.2:
                    print("%s: %s => %f" % (key, label, score))




if __name__ == '__main__':
    main()
