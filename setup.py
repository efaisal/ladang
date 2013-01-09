#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension

long_description = """A Python module which provides a binding to inotify API."""

setup(
    name = 'ladang',
    description = 'Yet another inotify binding',
    long_description = long_description,
    url = 'https://github.com/efaisal/ladang',
    version = '0.9.0',
    author = 'E A Faisal',
    author_email = 'eafaisal@gmail.com',
    license = 'MIT',
    package_dir = {'': 'src'},
    packages = [''],
    ext_modules = [Extension("_ladang", ["src/_ladang.c"])],
    platforms = ['Linux']
)
