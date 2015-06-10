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

``from epoch_analyzer import EpochTester``

If you desire you can pass a min_date and max_date which are used for reference.

Given the resulting object you can call test or convert, for either testing numbers for a probable format or (batch) converting lists of numbers to dates.

Usage EpochTester.test
----------------------

You can pass one number, an iterable list of numbers (for example a counter) to this method.

For each number one test conversion is performed, it then check which format matches most of the values, a counter object is returned. By calling most_common on that object, the items can be iterated in order starting at the most likely options.


.. code-block:: python

  from epoch_analyzer import EpochTester

  tester = EpochTester()
  results = tester.test({12345435, 231920232})

  for match, occurrence in result.most_common():
        print("t%s:\t%d%%" % (match, occurrence))


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

.. code-block:: sh

  For input 1394543556:
    Number Of Seconds Since Unix Epoch (2014-03-11 13:12:36)


Convert a list of timestamp from a file and output them to a file as unix timestamp.

``epoch -f input.txt -u > output-timestamps.txt``

Make a summary of the matches from a list of timestamps from a file.

``epoch -f input.txt --summary``

Output:

.. code-block:: sh

  Summary for 5 inputs:
  	1.	Number Of Seconds Since Unix Epoch:	40%
  	2.	Number Of Minutes Since Mac OSX Epoch:	40%
  	3.	Number Of Mili Seconds Since Unix Epoch:	20%

Supply a minimum (which is in this case out-of-range for this unixtime):

``epoch --min 2014-12-01 1394543556``

Output:

.. code-block:: sh

  For input 1394543556:
    No matching pattern was found

A space seperated hexadecimal input is supported:

``epoch "aa bb" --hex``

Output (Note that big and little endian are both tested):

.. code-block:: sh

  For input 48042:
  	No matching pattern was found
  For input 43707:
  	No matching pattern was found
