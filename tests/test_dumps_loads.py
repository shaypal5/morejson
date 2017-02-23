"""Testing the dumps and loads functionality."""

import unittest

import sys
import datetime
import json

import morejson


__author__ = "Shay Palachy"
__copyright__ = "Shay Palachy"
__license__ = "MIT"


class TestDumps(unittest.TestCase):
    """Testing the dumps and loads functionality."""

    def test_regular_dumps(self):
        """Testing dumps and loads of regular types."""
        dicti = {
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, json.loads(morejson.dumps(dicti)))

    def test_dumps_date(self):
        """Testing dumps and loads of date types."""
        dicti = {
            'date': datetime.date.today(),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_time(self):
        """Testing dumps and loads of time types."""
        dicti = {
            'mintime': datetime.time.min,
            'maxtime': datetime.time.max,
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_datetime(self):
        """Testing dumps and loads of datetime types."""
        dicti = {
            'datetime': datetime.datetime.now(),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_timedelta(self):
        """Testing dumps and loads of timedelta types."""
        dicti = {
            'timedelta1': datetime.timedelta(days=392),
            'timedelta2': datetime.timedelta(weeks=2, hours=23),
            'timedelta3': datetime.timedelta(microseconds=27836),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    @unittest.skipIf(sys.version_info < (3, 0), "not supported in Python2")
    def test_dumps_timezone(self):
        """Testing dumps and loads of timezone types."""
        dicti = {
            'utc_timezone': datetime.timezone.utc,
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_set(self):
        """Testing dumps and loads of set types."""
        dicti = {
            'set': set([1, 2, 4, 4, 2]),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_frozenset(self):
        """Testing dumps and loads of frozenset types."""
        dicti = {
            'frozenset': frozenset([1, 2, 4, 4, 2]),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

    def test_dumps_complex(self):
        """Testing dumps and loads of complex types."""
        dicti = {
            'complex1': complex(1, 34.2),
            'complex2': complex(-98.213, 91823),
            'array': [1, 2, 3],
            'string': 'trololo',
            'int': 1,
            'float': 4.32,
            'true': True,
            'false': False,
            'null': None
        }
        self.assertEqual(dicti, morejson.loads(morejson.dumps(dicti)))

