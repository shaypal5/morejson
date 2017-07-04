"""Core functionalities for morejson."""

import binascii
import datetime
import inspect
import json
import pickle
# noinspection PyUnresolvedReferences
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

try:
    import pytz
except ImportError:  # pragma: no cover
    # This installation doesn't have pytz, so we can ignore it
    pytz = None

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
    rv = {
        _MOREJSON_TYPE : _EncodedTypes.DATETIME,
        'year' : obj.year,
        'month' : obj.month,
        'day' : obj.day,
        'hour' : obj.hour,
        'minute' : obj.minute,
        'second' : obj.second,
        'microsecond' : obj.microsecond,
    }
    if obj.tzinfo:
        rv["tzinfo"] = _timezone_encoder(obj.tzinfo, dt=obj)
    return rv


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

# Pickle can be used to restore the exact class originally used by the timezone,
# but is potentially dangerous when accepting input from an untrusted source. Therefore it is
# disabled by default here. Without CONFIG['allow_pickle'] == True, a roundtrip with a pytz zone
# would turn it into a generic datetime.timezone with the same offset. That may be sufficient for
#  many purposes, but for example, it causes the unit test to fail because the input and output
# are different (though equivalent) classes. So if you need the exact TZ class returned in a
# roundtrip, you can set allow_pickle=True, but be wary of accepting JSON from untrusted sources.

CONFIG = {
    "allow_pickle": False,
}


def allow_pickle():
    return CONFIG.get("allow_pickle", False)


def _timezone_encoder(obj, dt=None):
    if dt is None:
        dt = datetime.datetime.now()
    rv = {
        _MOREJSON_TYPE: _EncodedTypes.TIMEZONE,
        'offset': obj.utcoffset(dt),
        'name': obj.tzname(dt),
    }
    if allow_pickle():
        # Hacky, but this allows us to restore the exact class that was used
        rv['__pickle__'] = binascii.b2a_base64(pickle.dumps(obj)).decode("ascii").strip()
    return rv


def _timezone_decoder(dict_obj):
    pickle_str = dict_obj.pop("__pickle__", None)
    if allow_pickle() and pickle_str:
        return pickle.loads(binascii.a2b_base64(pickle_str.encode("ascii")))
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
    PYTZ_TIMEZONE = 'pytz.tzinfo.BaseTzInfo'
    PYTZ_FIXEDOFFSET = 'pytz.FixedOffset'
    PYTZ_UTC = 'pytz.UTC'
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


if pytz is not None:  # pragma: no branch
    # pytz uses a different class for each zone, so we need the map key to be the base class
    # BaseTzInfo. Currently, pytz uses the same encoder/decoder as for 'datetime.timezone' as
    # well as the same __type__ - so you won't see PYTZ_TIMEZONE in the actual JSON. However if
    # necessary a different decoder could be used if they need to be split off.
    _ENCODER_MAP[pytz.tzinfo.BaseTzInfo] = _timezone_encoder
    _DECODER_MAP[_EncodedTypes.PYTZ_TIMEZONE] = _timezone_decoder

    # Pytz's UTC and FixedOffset class don't have the same base class as the others.
    _ENCODER_MAP[pytz.UTC.__class__] = _timezone_encoder
    _DECODER_MAP[_EncodedTypes.PYTZ_UTC] = _timezone_decoder

    _ENCODER_MAP[pytz._FixedOffset] = _timezone_encoder
    _DECODER_MAP[_EncodedTypes.PYTZ_FIXEDOFFSET] = _timezone_decoder

    # With Python 2.7 and pytz installed, we can decode "_EncodedTypes.TIMEZONE" with above types, but can't
    # encode `datetime.timezone` itself since it doesn't exist.
    _DECODER_MAP[_EncodedTypes.TIMEZONE] = _timezone_decoder


def _morejson_object_hook(dict_obj):
    try:
        if _MOREJSON_TYPE not in dict_obj:
            return dict_obj
        objtype = dict_obj.pop(_MOREJSON_TYPE)
        try:
            return _DECODER_MAP[objtype](dict_obj)
        except BaseException:
            dict_obj[_MOREJSON_TYPE] = objtype
            return dict_obj
    except TypeError:
        return dict_obj


def _get_wrapped_morejson_hook(custom_hook):
    def _wrapped_morejson_hook(dict_obj):
        first_res = custom_hook(dict_obj)
        return _morejson_object_hook(first_res)
    return _wrapped_morejson_hook


def _morejson_default_encoder(obj): # pylint: disable=E0202
    try:
        enc_key = type(obj)
        if pytz is not None and isinstance(obj, pytz.tzinfo.BaseTzInfo):
            enc_key = pytz.tzinfo.BaseTzInfo
        return _ENCODER_MAP[enc_key](obj)
    except KeyError:
        raise TypeError("Type {} is not JSON encodable.".format(type(obj)))


def _get_wrapped_morejson_default_encoder(custom_default):
    def _wrapped_morejson_default_encoder(obj):
        try:
            return custom_default(obj)
        except TypeError:
            return _morejson_default_encoder(obj)
    return _wrapped_morejson_default_encoder


# === wrapping the json api ===

def dump(obj, fp, **kwargs): # pylint: disable=C0103, C0111
    default_to_put = _morejson_default_encoder
    if 'default' in kwargs:
        default_to_put = _get_wrapped_morejson_default_encoder(
            kwargs.pop('default'))
    json.dump(obj, fp, default=default_to_put, **kwargs)


def dumps(obj, **kwargs): # pylint: disable=C0103, C0111
    default_to_put = _morejson_default_encoder
    if 'default' in kwargs:
        default_to_put = _get_wrapped_morejson_default_encoder(
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
