"""Testing the dump and load functionality."""

import unittest

import sys
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


class TestDump(unittest.TestCase):
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

    def test_dumps_datetime_with_fold(self):
        """Testing dump and load of datetime types."""
        if sys.version_info.major < 3 or sys.version_info.minor < 6:
            return
        try:
            dt = datetime.datetime(
                year=2012, month=10, day=10, fold=0.3)
            _build_test_dirs()
            dicti = {
                'datetime': dt,
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

    @unittest.skipIf(sys.version_info < (3, 0), "not supported in Python2")
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

    def test_load_bad_datetime_arg(self):
        """Testing dumps of unsupported types."""
        expected = {
            "release_day": 2,
            "closing_date": {
                "bad_arg": 12,
                "month": 10,
                "year": 2013,
                "day": 18,
                "__type__": "datetime.date"
            }
        }
        with open('tests/bad_datetime_arg.json', 'r') as json_file:
            self.assertEqual(expected, morejson.load(json_file))

    def test_load_unsupported_type(self):
        """Testing dump of unsupported types."""
        expected = {
            "name": "Kevin",
            "age": 21,
            "pet": {
                "name": "Trippy Jack",
                "age": 20762,
                "__type__": "hyperdimensional.hamster"
            }
        }
        with open('tests/unsupported_type.json', 'r') as json_file:
            self.assertEqual(expected, morejson.load(json_file))

    class _Monkey(object):
        def __init__(self, name, bananas):
            self.name = name
            self.bananas = bananas
        def __eq__(self, other):
            if isinstance(other, self.__class__):
                return (self.name == other.name) and (
                    self.bananas == other.bananas)
            else:
                return False

    @staticmethod
    def _monkey_default_encoder(obj): # pylint: disable=E0202
        if isinstance(obj, TestDump._Monkey):
            return {
                "_custom_type_": "monkey",
                "name": obj.name,
                "bananas": obj.bananas
            }
        else:
            raise TypeError("Type {} is not JSON encodable.".format(type(obj)))

    @staticmethod
    def _monkey_object_hook(dict_obj):
        if "_custom_type_" not in dict_obj:
            return dict_obj
        if dict_obj["_custom_type_"] == "monkey":
            return TestDump._Monkey(
                dict_obj['name'], dict_obj['bananas'])
        else:
            return dict_obj

    def test_dump_monkey(self):
        """Testing dumps of monkey types."""
        try:
            _build_test_dirs()
            johnny = TestDump._Monkey("Johnny", 54)
            dicti = {"my_pet": johnny}
            with open(_TEST_FILE, 'w+') as fileobj:
                morejson.dump(
                    dicti, fileobj, default=TestDump._monkey_default_encoder)
            with open(_TEST_FILE, 'r') as fileobj:
                res = morejson.load(
                    fileobj, object_hook=TestDump._monkey_object_hook)
                self.assertEqual(dicti, res)
        finally:
            _dismantle_test_dirs()
