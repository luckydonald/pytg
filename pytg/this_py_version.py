# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'luckydonald'
import sys

if sys.version < '3': # python 2.7
	is3 = False
else: # python 3
	is3 = True


import types
if not is3:
	def set_docstring(func, doctring):
		func.func_doc = doctring
else: #py3
	def set_docstring(func, doctring):
		func.__doc__ = doctring