=============================
Welcome to the Epoch Analyzer
=============================

.. image:: https://travis-ci.org/martinvw/epoch-analyzer.png?branch=master
    :target: https://travis-ci.org/martinvw/epoch-analyzer

.. image:: https://coveralls.io/repos/martinvw/epoch-analyzer/badge.png?branch=master
  :target: https://coveralls.io/r/martinvw/epoch-analyzer?branch=master

A python module to analyze numbers to determine on which epoch they might be based and in what unit they might be expressed.

Installation
------------

1. Install using pip:

   ``pip install epoch_analyzer``

   for windows:

   ``py -m pip install epoch_analyzer``

   Alternatively, you can download or clone this repo and call ``pip install -e .``.

Usage in Python
---------------

Import the EpochTester from the package epoch_analyzer

from epoch_analyzer import EpochTester

If you desire you can pass a min_date and max_date which are used for reference.

Given the resulting object you can call test or convert, for either testing numbers for a probable format or (batch) converting lists of numbers to dates.

Usage EpochTester.test
----------------------

You can pass one number, an iterable list of numbers (for example a counter) to this method.

For each number one test conversion is performed, it then check which format matches most of the values, the likely options are listed in order likelyhood

Usage EpochTester.convert
-------------------------

Lorem ipsum


Usage from the command line
---------------------------

When the module is correctly installed, the command `epoch` should be available from your path. There are a lot of options, which are listed calling the command without any argument.

Some examples:

Just convert a single value:

``epoch 1394543556``

Output:

.. code-block:: guess

  For input 1394543556:
    Number Of Seconds Since Unix Epoch (2014-03-11 13:12:36)


Convert a list of timestamp from a file and output them to a file as unix timestamp.

``epoch -f input.txt -u > output-timestamps.txt``

Make a summary of the matches from a list of timestamps from a file.

``epoch -f input.txt --summary``

....

Supply a minimum:

``epoch --min 2013-12-01 1394543556``
