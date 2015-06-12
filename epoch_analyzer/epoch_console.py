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
    parser.add_argument('--unixtime', '-u', action='store_true', help='show dates as unixtime.')
    parser.add_argument('--hex', action='store_true', help='Process the input as hexadecimal, tests for little and big endian.')
    # optional force an endianess

    parser.add_argument('--file', '-f', required=False, help='a file containing numeric times to be converted', type=argparse.FileType('r'))
    parser.add_argument('numbers', nargs='*', help='supply the input to analyze')

    args = parser.parse_args()

    tester = EpochTester(args.min, args.max)
    numbers = get_input_numbers(parser, args)

    if args.summary:
        print_summary(numbers, tester, args)
    elif not sys.stdout.isatty():
        print_to_pipe(numbers, tester, args)
    else:
        print_conversion(numbers, tester, args)

def valid_date(s):
    try:
        return datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)

def get_input_numbers(parser, args):
    if args.file and len(args.numbers) > 0:
        print("Warning: a file and commandline option given, using only file input!")

    numbers = []
    if args.file:
        for number in args.file:
            convert_numbers(numbers, number, args.hex)
    elif len(args.numbers) > 0:
        for number in args.numbers:
            convert_numbers(numbers, number, args.hex)
    else:
        print("Error: supply either a file with numbers or a list of numbers.")
        parser.print_help()
        sys.exit()

    return numbers

def convert_numbers(numbers, number, hex):
    number = number.strip()
    if not hex:
        numbers.append(float(number))
    else:
        number = re.sub(r"\s", '', number)
        byte_string = binascii.unhexlify((bytes(number, 'utf-8')))
        numbers.append(int.from_bytes(byte_string, byteorder='little'))
        numbers.append(int.from_bytes(byte_string, byteorder='big'))
        return

    # handle errors for the value conversion

def print_summary(numbers, tester, args):
    print("Summary for %d inputs:" % len(numbers))
    result = tester.test(numbers, True)
    counter = 1

    for i, j in result.most_common():
        print("\t%d.\t%s:\t%d%%" % (counter, i, j))
        counter += 1

def print_to_pipe(numbers, tester, args):
    result = tester.convert(numbers)
    for number, matches in result.items():
        if matches and len(matches) > 0:
            if args.unixtime:
                print(matches[0][1].timestamp())
            else:
                print("%s" % (matches[0][1]))
        else:
            print(None)

def print_conversion(numbers, tester, args):
    result = tester.convert(numbers)

    for number, matches in result.items():
        print("For input %d:" % number)
        if matches == None or len(matches) == 0:
            print("\tNo matching pattern was found")
        else:
            for match, date in matches:
                print("\t%s (%s)" % (match, date))
                if args.unixtime:
                    print("\tUnixtimestamp: %d" % date.timestamp())

if __name__ == '__main__':
    main()
