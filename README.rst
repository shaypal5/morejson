morejson
#########
``morejson`` is a drop-in replacement for Python's ``json`` module that handles additional built-in and standard library Python types.

.. code-block:: python

  import morejson as json
  import datetime

  json.dumps({'now': datetime.datetime.now()})
  json.dumps({'set': set([1,2], 'complex': complex(32, -4)})

.. contents::

.. section-numbering::


Installation
============

Install ``morejson`` with:

.. code-block:: bash

  pip install morejson


Use
===

``morejson`` implements the exact same API as Python'a built-in ``json`` module; the ``dump``, ``dumps``, ``load`` and ``loads`` methods wrap around their ``json`` counterparts without changing their interface, while any other function or attribute is left unchanged.

You can use any argument of these methods, including ``default``, ``cls`` and ``object_hook`; `morejson` will wrap around any kind of custom behaviour you provide, giving it priority over `morejson`'s encoding or decoding, and allowing you to use it with any custom JSON encoding/decoding code you created.


Supported Types
===============

Built-in Types
--------------

* set
* frozenset
* complex

datetime module types
---------------------

* date
* time
* datetime
* timedelta
* timezone

