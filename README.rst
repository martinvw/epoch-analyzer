=============================
Welcome to the Epoch Analyzer
=============================
.. image:: https://badge.fury.io/py/epoch_analyzer.svg
    :target: https://badge.fury.io/py/epoch_analyzer

.. image:: https://img.shields.io/pypi/status/epoch_analyzer.svg?maxAge=2592000   
    :target: https://pypi.python.org/pypi/epoch_analyzer

.. image:: https://travis-ci.org/martinvw/epoch-analyzer.png?branch=master
    :target: https://travis-ci.org/martinvw/epoch-analyzer

.. image:: https://coveralls.io/repos/martinvw/epoch-analyzer/badge.png?branch=master
    :target: https://coveralls.io/r/martinvw/epoch-analyzer?branch=master
  
.. image:: https://img.shields.io/pypi/pyversions/epoch_analyzer.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/epoch_analyzer

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
  results = tester.test({12345435, 2999663906})

  for match, occurrence in results.most_common():
        print("\t%s:\t%d%%" % (match, occurrence))


Usage EpochTester.convert
-------------------------

If you have an unknown type and want conversion to all plausible options you can use this method. If you already know the format its better to fetch a convertor and use that, see alse the option described below.

.. code-block:: python

  from epoch_analyzer import EpochTester

  tester = EpochTester()
  results = tester.convert({12345435, 2999663906})

  for input, matches in results.items():
    print("%d: #%d matches" % (input, len(matches)))

    for label, result in matches:
      print("\t%s:\t%s%%" % (label, result))

Output:

.. code-block:: sh

  2999663906: #1 matches
  	 4-Bytes bit-based timestamp since 1970:	2014-11-05 19:52:34%
  12345435: #0 matches


Usage for specific conversions
------------------------------

If you know with which epoch you are working and you are converting single numbers than the conversion is quite simple. In that case you don't have to use the convert method but you just request the specific convertor and use that, see the following example.

.. code-block:: python

  from epoch_analyzer import EpochTester

  convertor = EpochTester().get_convertor('4-Bytes bit-based timestamp since 1970')

  print(convertor.convert_to_date(2999663906)) # prints '2014-11-05 19:52:34'


Usage from the command line
---------------------------

When the module is correctly installed, the command `epoch` should be available from your path. There are a lot of options, which are listed when calling the command without any arguments.

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

A space separated hexadecimal input is supported:

``epoch "aa bb" --hex``

Output (Note that big and little endian are both tested):

.. code-block:: sh

  For input 48042:
  	No matching pattern was found
  For input 43707:
  	No matching pattern was found


Usage from the command line: scanning binary files
--------------------------------------------------

When the module is correctly installed (note that termcolor is a prerequisite), the command `epoch_scan` should be available from your path. There are a lot of options, which are listed when calling the command without any arguments.

The table width is required to make columns and spot patterns. If your data has a fixed table width its most of the time easy to detect by just resizing your hex editor until you see clear columns of repeating or similair data being displayed. Compare the following two examples:

.. code-block::

   ª..!B....tI.v..:r.#..gd.....l...._..2..9D.a..T..d...ª..!B ........
   .wª..!B....tI.w..9r.#..gd.....l...._..2..9D.a..T..d...ª..!B ......
   ...wª..!B....tI.w..9r.#..gd.....l...._..2..9D.a..T..d...ª..!B ....
   .....wª..!B....tI.w..9q."..id.....l...._..2..9D.a..T..d...ª..!B ..
   .......wª..!B....tI.w..9q."..id.....l...._..2..9D.a..T..d...ª..!B 
   .........w
   
.. code-block::

   ª..!B....tI.v..:r.#..gd.....l...._..2..9D.a..T..d...ª..!B .........w
   ª..!B....tI.w..9r.#..gd.....l...._..2..9D.a..T..d...ª..!B .........w
   ª..!B....tI.w..9r.#..gd.....l...._..2..9D.a..T..d...ª..!B .........w
   ª..!B....tI.w..9q."..id.....l...._..2..9D.a..T..d...ª..!B .........w
   ª..!B....tI.w..9q."..id.....l...._..2..9D.a..T..d...ª..!B .........w

Some examples:

Scan for epoch values in the file above:

``epoch_scan -t 44 raw.log``

Output:

.. code-block:: sh

    Sample picked from offset: 4
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (big end.)      22282752        =>   1970-05-10 00:08:00    4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (little end.)   1677722196      =>   None                   4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (little end.)   -1441202176     =>   2012-08-12 16:00:00    4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (little end.)   1109458944      =>   1986-08-16 16:00:00    4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (big end.)      -1441791967     =>   2012-08-08 00:00:33    4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (little end.)   1109458960      =>   1986-08-16 16:00:16    4-Bytes bit-based timestamp since 1970 [0.900000]
    44036102 01540200 64000019 AA000021 42200005 00000000 00000077 AA100021 42100001 07744901 77000539      (little end.)   117506064       =>   None                   4-Bytes bit-based timestamp since 1970 [0.900000]
    
The outputs shows a random sample from the file. Each match is highlighted (blue for big endian, green for little endian). The bytes are shown in capital hex and displayed in groups of 4 bytes. To aid the interpretation of the results, both the numeric value and the converted value are shown for the matching format.

Other options which might be helpfull are:

* using a fixed sample -s
* defining a --min or --max if you expect a specific period
* limit the number of items to process -c
