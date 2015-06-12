import unittest
import datetime
import subprocess

from epoch_analyzer import EpochTester

class ConsoleTest(unittest.TestCase):
    def setUp(self):
        pass

    def check_output(self, cmd, *args, **kwargs):
        result = subprocess.check_output(cmd, *args, **kwargs)
        if result:
            result = result.decode('UTF-8')
        return result

    def test_single_value(self):
        result = self.check_output(['epoch', '--min', '2010-01-01', '1394543556'])
        self.assertEqual("2014-03-11 13:12:36",  result.strip())

    def test_single_value_fail(self):
        result = self.check_output(['epoch', '--min', '2015-01-01', '1394543556'])
        self.assertEqual("None",  result.strip())

    def test_hex_value(self):
        result = self.check_output(['epoch', 'A2 3A E8 44', '--hex', '--min', '2010-01-01', '--max', '2015-01-01'])
        i = 0

        for line in result.splitlines():
            i == 0 and self.assertEqual("2014-07-08 07:21:04",  line)
            i == 1 and self.assertEqual("2010-08-29 14:33:04",  line)

            i += 1

        ## also try it the other way around
        result = self.check_output(['epoch', '44 E8 3A A2', '--hex', '--min', '2010-01-01', '--max', '2015-01-01'])
        i = 0

        for line in result.splitlines():
            i == 1 and self.assertEqual("2014-07-08 07:21:04",  line)
            i == 0 and self.assertEqual("2010-08-29 14:33:04",  line)

            i += 1
