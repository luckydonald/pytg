#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

long_description = """A Python module that wraps around Telegram messenger CLI, Version 2, forked and updated from https://github.com/efaisal/pytg"""

try:
   from distutils.command.build_py import build_py_2to3 \
        as build_py
except ImportError:
   from distutils.command.build_py import build_py

setup(
    name = 'pytg',
    description = 'Telegram messenger CLI wrapper 2',
    long_description = long_description,
    url = 'https://bitbucket.org/luckydonald/pytg2',
    cmdclass = {'build_py': build_py},
    version = '0.2.2',
    author = 'luckydonald (forked from E A Faisal)',
    author_email = 'luckydonald@flutterb.at',
    license = 'MIT',
    packages = ['pytg'],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Programming Language :: Python",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
    ]
)
