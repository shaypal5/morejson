"""A wrapper for Python's json module supporting Python built-in types."""

from .core import  *  # pylint: disable=W0401
try:
    del datetime
    del inspect
    del json
    del core
except BaseException:
    pass

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
