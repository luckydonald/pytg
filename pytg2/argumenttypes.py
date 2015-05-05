__author__ = 'luckydonald'
from . import encoding
from os import path # file checking.

import logging
logger = logging.getLogger(__name__)

class UnknownFunction(Exception):
	pass


def none(value):
	if value == None:
		return True
	return False

def peer(value):
	if not unescaped_unicode_string(value):
		return False
	if " " in value:
		return False
	return True

def chat(value):
	if not peer(value):
		return False
	return True

def user(value):
	return peer(value)

def secret_chat(value):
	return peer(value)

def unicode_string(value):
	return isinstance(value, encoding.text_type) #TODO

def unescaped_unicode_string(value):
	"""
	Used for unicodes stings which will not be escaped.
	"""
	return isinstance(value, encoding.text_type)

def number(value):
	return isinstance(value, (int, encoding.long_int))

def double(value):
	return isinstance(value, float)

def positive_number(value):
	if number(value):
		if value > 0:
			return True
	return False

def file(value):
	logger.debug("Got file: [{}]".format(value)) #TODO remove
	return path.isfile(encoding.native_type(value))

def nonnegative_number(value):
	if number(value):
		if value >= 0:
			return True
	return False

def msg_id(value):
	if unicode_string(value):
		try:
			int_val = int(value)
			return positive_number(int_val)
		except:
			return False
	return positive_number(value)

def optional():
	return True

from .utils import escape
def validate_input(function_name, arguments, arguments_types):
		if (len(arguments) != len(arguments_types)):
			raise ValueError("Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(function_name=function_name, expected_number=len(arguments_types), given_number=len(args)))
		i = 0
		new_args = []
		for arg in arguments:
			func_type = arguments_types[i]
			# arg is the given one, which should be func_type.
			if not func_type(arg):
				raise ValueError("Error in function {function_name}: parameter {number} is not type {type}.".format(function_name=function_name, number=i, type=func_type.__name__))
			if func_type == unicode_string:
				new_args.append(encoding.to_unicode(escape(arg)))
			else:
				new_args.append(encoding.to_unicode(str(arg)))
			i += 1
		# end for
		return new_args