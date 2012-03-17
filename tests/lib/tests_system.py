#!/usr/bin/python2

import unittest

from pycious.lib.system import battery, cpu, mem_usage, date, \
    network_statistics

class BatteryTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_battery_status(self):
        self.assertIs(battery()[0], str)

if __name__ == "__main__":
    unittest.main()
