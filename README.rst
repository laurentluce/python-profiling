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

We have the following function that we want to benchmark and profile.

.. code-block:: python

    def hash(s):
        h = hashlib.sha256()
        h.update(s)
        return h.digest()


This function is located in examples.py.

Our config file should look like:

.. code-block:: json

    [
        {"func": "examples.hash",
         "args": "profiling_examples.get_hash_args",
         "rounds": 1000000
        }
    ]

We need to write a function to provide arguments to our function hash.  To do that, we add the following function to our profiling_examples.py module.

.. code-block:: python

    def get_hash_args():
        return ('that dog runs fast.',)

As you can see, the function returns a tuple of arguments to pass to our function hash during profiling and benchmarking.

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

We can see that each round of the function hash took about 1.3 ms.  Most of the time (71%) was spent in the method haslib.digest.
