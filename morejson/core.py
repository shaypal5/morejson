"""Core functionalities for morejson."""

import datetime
import inspect
import json
from json import (  # pylint: disable=W0611
    decoder,
    encoder,
    JSONDecoder,
    JSONEncoder,
    scanner,
    _default_decoder,
    _default_encoder
)
try:
    from json import (  # pylint: disable=W0611
        JSONDecodeError
    )
except ImportError:
    pass # we're on Python 2/3.4 or below


# partly based on a great git gist by abhinav-upadhyay:
# https://gist.github.com/abhinav-upadhyay/5300137


# === date ===

def _date_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.DATE,
        'year' : obj.year,
        'month' : obj.month,
        'day' : obj.day
    }

def _date_decoder(dict_obj):
    return datetime.date(**dict_obj)


# === time ===

def _time_encoder(obj):
    dict_obj = {
        _MOREJSON_TYPE : _EncodedTypes.TIME,
        'hour' : obj.hour,
        'minute' : obj.minute,
        'second' : obj.second,
        'microsecond' : obj.microsecond,
        'tzinfo' : obj.tzinfo
    }
    if hasattr(obj, 'fold'):
        dict_obj['fold'] = obj.fold
    return dict_obj

def _time_decoder(dict_obj):
    return datetime.time(**dict_obj)


# === datetime ===

def _datetime_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.DATETIME,
        'year' : obj.year,
        'month' : obj.month,
        'day' : obj.day,
        'hour' : obj.hour,
        'minute' : obj.minute,
        'second' : obj.second,
        'microsecond' : obj.microsecond,
    }

def _datetime_decoder(dict_obj):
    return datetime.datetime(**dict_obj)


# === timedelta ===

def _timedelta_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.TIMEDELTA,
        'days' : obj.days,
        'seconds' : obj.seconds,
        'microseconds' : obj.microseconds
    }

def _timedelta_decoder(dict_obj):
    return datetime.timedelta(**dict_obj)


# === timezone ===

def _timezone_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.TIMEZONE,
        'offset' : obj.utcoffset(datetime.datetime.now()),
        'name' : obj.tzname(datetime.datetime.now())
    }

def _timezone_decoder(dict_obj):
    return datetime.timezone(**dict_obj)


# === set ===

def _set_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.SET,
        'members' : list(obj)
    }

def _set_decoder(dict_obj):
    return set(dict_obj['members'])


# === frozenset ===

def _frozenset_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.FROZENSET,
        'members' : list(obj)
    }

def _frozenset_decoder(dict_obj):
    return frozenset(dict_obj['members'])


# === complex ===

def _complex_encoder(obj):
    return {
        _MOREJSON_TYPE : _EncodedTypes.COMPLEX,
        'real': obj.real,
        'imag' : obj.imag
    }

def _complex_decoder(dict_obj):
    return complex(dict_obj['real'], dict_obj['imag'])


# === morejson endocer and decoder ===

_MOREJSON_TYPE = '__type__'

class _EncodedTypes(object):
    DATE = 'datetime.date'
    TIME = 'datetime.time'
    DATETIME = 'datetime.datetime'
    TIMEDELTA = 'datetime.timedelta'
    TIMEZONE = 'datetime.timezone'
    SET = 'set'
    FROZENSET = 'frozenset'
    COMPLEX = 'complex'

_ENCODER_MAP = {
    datetime.date: _date_encoder,
    datetime.time: _time_encoder,
    datetime.datetime: _datetime_encoder,
    datetime.timedelta: _timedelta_encoder,
    set: _set_encoder,
    frozenset: _frozenset_encoder,
    complex: _complex_encoder
}

_DECODER_MAP = {
    _EncodedTypes.DATE: _date_decoder,
    _EncodedTypes.TIME: _time_decoder,
    _EncodedTypes.DATETIME: _datetime_decoder,
    _EncodedTypes.TIMEDELTA: _timedelta_decoder,
    _EncodedTypes.SET: _set_decoder,
    _EncodedTypes.FROZENSET: _frozenset_decoder,
    _EncodedTypes.COMPLEX: _complex_decoder
}

try:
    _ENCODER_MAP[datetime.timezone] = _timezone_encoder
    _DECODER_MAP[_EncodedTypes.TIMEZONE] = _timezone_decoder
except AttributeError:
    pass  # we're on Python 2.x


def _morejson_object_hook(dict_obj):
    if _MOREJSON_TYPE not in dict_obj:
        return dict_obj
    objtype = dict_obj.pop(_MOREJSON_TYPE)
    try:
        return _DECODER_MAP[objtype](dict_obj)
    except BaseException:
        dict_obj[_MOREJSON_TYPE] = objtype
        return dict_obj


def _get_wrapped_morejson_hook(custom_hook):
    def _wrapped_morejson_hook(dict_obj):
        first_res = custom_hook(dict_obj)
        return _morejson_object_hook(first_res)
    return _wrapped_morejson_hook


def _morejson_defualt_encoder(obj): # pylint: disable=E0202
    try:
        return _ENCODER_MAP[type(obj)](obj)
    except KeyError:
        raise TypeError("Type {} is not JSON encodable.".format(type(obj)))


def _get_wrapped_morejson_defualt_encoder(custom_default):
    def _wrapped_morejson_defualt_encoder(obj):
        try:
            return custom_default(obj)
        except TypeError:
            return _morejson_defualt_encoder(obj)
    return _wrapped_morejson_defualt_encoder


# === wrapping the json api ===

def dump(obj, fp, **kwargs): # pylint: disable=C0103, C0111
    default_to_put = _morejson_defualt_encoder
    if 'default' in kwargs:
        default_to_put = _get_wrapped_morejson_defualt_encoder(
            kwargs.pop('default'))
    json.dump(obj, fp, default=default_to_put, **kwargs)


def dumps(obj, **kwargs): # pylint: disable=C0103, C0111
    default_to_put = _morejson_defualt_encoder
    if 'default' in kwargs:
        default_to_put = _get_wrapped_morejson_defualt_encoder(
            kwargs.pop('default'))
    return json.dumps(obj, default=default_to_put, **kwargs)


def load(fp, **kwargs): # pylint: disable=C0103, C0111
    hook_to_put = _morejson_object_hook
    if 'object_hook' in kwargs:
        hook_to_put = _get_wrapped_morejson_hook(kwargs.pop('object_hook'))
    return json.load(fp, object_hook=hook_to_put, **kwargs)


def loads(s, **kwargs): # pylint: disable=C0103, C0111
    hook_to_put = _morejson_object_hook
    if 'object_hook' in kwargs:
        hook_to_put = _get_wrapped_morejson_hook(kwargs.pop('object_hook'))
    return json.loads(s, object_hook=hook_to_put, **kwargs)


_FUNC_MAP = {
    dump: json.dump,
    dumps: json.dumps,
    load: json.load,
    loads: json.loads
}

for _func in _FUNC_MAP:
    _func.__doc__ = _FUNC_MAP[_func].__doc__
    try:
        _func.__signature__ = inspect.signature(_FUNC_MAP[_func])
    except AttributeError:
        pass  # we're on python 2/3.3 or lower
