#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.extension import Extension

long_description = """A Python module that wraps around Telegram messenger CLI."""

setup(
    name = 'pytg',
    description = 'Telegram messenger CLI wrapper',
    long_description = long_description,
    url = 'https://github.com/efaisal/pytg',
    version = '0.1',
    author = 'E A Faisal',
    author_email = 'eafaisal@gmail.com',
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
