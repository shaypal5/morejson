"""Testing the dump and load functionality."""

from unittest import TestCase

import os
import datetime
import json

import morejson


__author__ = "Shay Palachy"
__copyright__ = "Shay Palachy"
__license__ = "MIT"


_HOMEDIR = os.path.expanduser("~")
_TEST_FOLDER = os.path.join(_HOMEDIR, '.morejson_test')
_TEST_FILE = os.path.join(_TEST_FOLDER, 'test.json')


def _build_test_dirs():
    try:
        os.mkdir(_TEST_FOLDER)
    except FileExistsError:
        pass


def _dismantle_test_dirs():
    try:
        for filename in os.listdir(_TEST_FOLDER):
            file_path = os.path.join(_TEST_FOLDER, filename)
            os.remove(file_path)
        os.rmdir(_TEST_FOLDER)
    except PermissionError:
        pass  # mac is annoying


class TestDump(TestCase):
    """Testing the dump and load functionality."""

    def test_regular_dump(self):
        """Testing dump and load of regular types."""
        try:
            _build_test_dirs()
            dicti = {
                'array': [1, 2, 3],
                'string': 'trololo',
                'int': 1,
                'float': 4.32,
                'true': True,
                'false': False,
                'null': None
            }
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, json.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_date(self):
        """Testing dump and load of date types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_time(self):
        """Testing dump and load of time types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_datetime(self):
        """Testing dump and load of datetime types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_timedelta(self):
        """Testing dump and load of timedelta types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_timezone(self):
        """Testing dump and load of timeone types."""
        try:
            _build_test_dirs()
            dicti = {
                'utctimezone': datetime.timezone.utc,
                'array': [1, 2, 3],
                'string': 'trololo',
                'int': 1,
                'float': 4.32,
                'true': True,
                'false': False,
                'null': None
            }
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_set(self):
        """Testing dump and load of set types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_frozenset(self):
        """Testing dump and load of frozenset types."""
        try:
            _build_test_dirs()
            dicti = {
                'set': frozenset([1, 2, 4, 4, 2]),
                'array': [1, 2, 3],
                'string': 'trololo',
                'int': 1,
                'float': 4.32,
                'true': True,
                'false': False,
                'null': None
            }
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

    def test_dumps_complex(self):
        """Testing dump and load of complex types."""
        try:
            _build_test_dirs()
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
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(dicti, fileobj)
            with open(_TEST_FILE, 'r') as fileobj:
                self.assertEqual(dicti, morejson.load(fileobj))
        finally:
            _dismantle_test_dirs()

