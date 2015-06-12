#!/usr/bin/env python
import os
import sys

from setuptools import setup


def get_metadata():
    import re
    with open(os.path.join("epoch_analyzer", "__init__.py")) as f:
        return dict(re.findall("__([a-z]+)__ = ['\"]([^'\"]+)['\"]", f.read()))

metadata = get_metadata()

if sys.argv[-1] == 'publish':
    os.system('cd docs && make html')
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (metadata['version'], metadata['version']))
    print("  git push --tags")
    sys.exit()

try:
    long_description = open("README.rst", "r").read()
except Exception:
    long_description = None

setup(
    name='epoch_analyzer',
    version=metadata['version'],
    license='MIT',
    packages=['epoch_analyzer'],
    author='Martin van Wingerden',
    author_email='martinvw@mtin.nl',
    url='https://github.com/martinvw/epoch-analyzer',
    download_url='https://github.com/martinvw/epoch-analyzer/tarball/v' + metadata['version'],
    description='Utility detect probable date/time formats given a numeric input.',
    long_description=long_description,
    entry_points={'console_scripts': ['epoch = epoch_analyzer.epoch_console:main']},
    include_package_data=True,
    install_requires=[],
    keywords=['datetime', 'timestamp', 'epoch'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: System :: Filesystems',
        'Development Status :: 4 - Beta',
        'Topic :: Terminals',
        'Topic :: Utilities',
    ],
)
