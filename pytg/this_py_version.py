# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import types

__author__ = 'luckydonald'

if sys.version < '3':  # python 2.7
    is3 = False
else:  # python 3
    is3 = True

if not is3:  # py2
    def set_docstring(func, doctring):
        func.func_doc = doctring


    def set_kwdefaults(func, kwdefaults):
        func.func_kwdefaults = kwdefaults


    def get_dict_items(dict):
        return dict.viewitems()

else:  # py3
    def set_docstring(func, doctring):
        func.__doc__ = doctring


    def set_kwdefaults(func, kwdefaults):
        func.__kwdefaults__ = kwdefaults


    def get_dict_items(dict):
        return dict.items()
