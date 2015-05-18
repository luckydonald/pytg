# -*- coding: utf-8 -*-
__author__ = 'luckydonald'
import logging
logger = logging.getLogger(__name__)


#sender.py
class NoResponse(Exception):
	pass

#sender.py
class ConnectionError(NoResponse):
	pass


#sender.py
class UnknownFunction(Exception):
	pass

#result_parser.py/sender.py
class IllegalResponseException(Exception):
	pass

#argument_types.py
class ArgumentParseError(Exception):
	pass