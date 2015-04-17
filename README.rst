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

   ``pip install epoch-analyzer``

   Alternatively, you can download or clone this repo and call ``pip install -e .``.

Usage in Python
---------------

Import the EpochTester from the package epoch_analyzer

from epoch_analyzer import EpochTester

If you desire you can pass a min_date and max_date which are used for reference.

Given the resulting object you can call test or convert, for either testing numbers for a probable format or (batch) converting lists of numbers to dates.

Usage EpochTester.test
----------------------
You can pass one number, an iterable list of numbers or for example a counter to this method.

For each number one test conversion is performed 
