from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="datetimex",
    version="1.1.0",
    author="greenlotusx",
    author_email="greenlotusx@163.com",
    description="A Python library that formats strings with date and time.",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/GreenLotusx/DateTimex",
    packages=['datetimex'],
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ),
    zip_safe=True,
)