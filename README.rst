================
Python Profiling
================

Overview
========

Benchmark and profile functions and methods with no code modification or inlining/decoration.

Requirements
============

Python 2.7

Function benchmarking and profiling
===================================

We have the following hashing function that we want to benchmark and profile.  The function uses SHA-256 and returns the hashed string.

.. code-block:: python

    def hash(s):
        h = hashlib.sha256()
        h.update(s)
        return h.digest()


This function is located in examples.py.

We need to write a function to provide arguments to our function ``hash`` during benchmarking and profiling. To do that, we add the following function to our profiling_examples.py module so we keep profiling inputs separated from the actual code.

.. code-block:: python

    def get_hash_args():
        return ('that dog runs fast.',), {}

As you can see, the function returns a tuple with a list of arguments and a list of keyword arguments to pass to our function ``hash`` during profiling and benchmarking.

Our config file ``config.txt`` should look like:

.. code-block:: json

    [
        {"func": "examples.hash",
         "args": "profiling_examples.get_hash_args",
         "rounds": 1000000
        }
    ]

We can now run profiling and benchamrking.

.. code-block:: bash

    $ python profiling.py config.txt

    {'exception': None,
     'name': u'examples.hash',
     'time': 0.0012605090141296386,
     'time_diff_percentage': None,
     'top_calls_total_time': [{'name': 'hash', 'percentage': 100.0},
                              {'name': "<method 'digest' of '_hashlib.HASH' objects>",
                               'percentage': 71.14931422310623},
                              {'name': '<_hashlib.openssl_sha256>',
                               'percentage': 33.92688263906788},
                              {'name': "<method 'update' of '_hashlib.HASH' objects>",
                               'percentage': 31.19609717628527},
                              {'name': '<range>',
                               'percentage': 0.6900382909640923}]}

By looking at ``time``, we can see that each round of the function ``hash`` took about 0.0013 ms.  Looking at the list ``top_calls_total_time``, we can see that most of the time (71%) is spent in the method ``hashlib.digest``.

We would like to see the performance impact of switching from sha256 to sha512.  To do that, we modify our function ``hash`` to use sha512 and use run our benchmarking and profiling one more time.

.. code-block:: python

    def hash(s):
        h = hashlib.sha512()
        h.update(s)
        return h.digest()

.. code-block:: bash

    $ python profiling.py config.txt

    {'exception': None,
     'name': u'examples.hash',
     'time': 0.001597745180130005,
     'time_diff_percentage': 26.753967026028963,
     'top_calls_total_time': [{'name': "<method 'digest' of '_hashlib.HASH' objects>",
                               'percentage': 100.0},
                              {'name': 'hash', 'percentage': 97.52547754489723},
                              {'name': '<_hashlib.openssl_sha512>',
                               'percentage': 33.28412780886871},
                              {'name': "<method 'update' of '_hashlib.HASH' objects>",
                               'percentage': 31.70173960897455},
                              {'name': '<range>',
                               'percentage': 0.6164936789949396}]}

Looking at ``time_diff_percentage``, we can see that switching from sha256 to sha512 added 27% to the runtime.

Method benchmarking and profiling
=================================

If ``hash`` is a method instead of a function, we need to modify our config file and we need to provide the arguments required to create an instance of the class which has the method ``hash``.

Our method ``hash`` in the class ``Crypto`` looks like this:

.. code-block:: python

    class Crypto(object):
        def __init__(self, algorithm):
            self.hash_algorithm = algorithm

        def hash(self, s):
            h = getattr(hashlib, self.hash_algorithm)()
            h.update(s)
            return h.digest()

We define a function in profiling_examples.py to provide arguments when the tool needs to instantiate a ``Crypto`` object:

.. code-block:: python

    def get_crypto_init_args():
        return ('sha256',), {}

Next is our config file:

.. code-block:: json

    [
        {"class": "examples.Crypto",
         "init_args": "profiling_examples.get_crypto_init_args",
         "method": "hash",
         "args": "profiling_examples.get_hash_args",
         "rounds": 1000000
        }
    ]

We can now run the benchmarking and profiling:

$ python profiling.py config.txt

.. code-block:: bash

    {'exception': None,
     'name': u'examples.Crypto.hash',
     'time': 0.001298166036605835,
     'time_diff_percentage': None,
     'top_calls_total_time': [{'name': 'hash', 'percentage': 100.0},
                              {'name': "<method 'digest' of '_hashlib.HASH' objects>",
                               'percentage': 53.16820861239049},
                              {'name': '<_hashlib.openssl_sha256>',
                               'percentage': 25.778153395074117},
                              {'name': "<method 'update' of '_hashlib.HASH' objects>",
                               'percentage': 25.675225862195138},
                              {'name': '<getattr>',
                               'percentage': 16.581719975731765}]}
