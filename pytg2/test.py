#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
def test():
	import pytg2
	import doctest
	returned = doctest.testmod(pytg2)
	return returned.failed

if __name__ == '__main__':
	sys.exit(test())