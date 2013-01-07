#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

long_description = """A Python module which provides a very thin layer binding to inotify API supporting both blocking and non-blocking operation."""

setup(
    name = 'ladang',
    description = 'Yet another inotify binding',
    long_description = long_description,
    url = 'http://code.google.com/p/ladang/',
    version = '0.7.0',
    author = 'E A Faisal',
    author_email = 'eafaisal@gmail.com',
    license = 'MIT',
    py_modules = ['ladang'],
    ext_modules = [Extension("ladang", ["src/ladang.c"])],
    platforms = ['Linux']
)
