# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from . import encoding
from .utils import escape  # validate_input
from .exceptions import ArgumentParseError
from os import path # file checking.
import logging
logger = logging.getLogger(__name__)


class Argument(object):
	def __init__(self, name, optional=False, multible=False):
		self.name = name
		self.optional = optional
		self.multible = multible

	def __str__(self):
		string = self.name
		if self.optional:
			string = "["+string+"]"
		else:
			string = "<"+string+">"
		if self.multible:
			string = string + "+"
		return string

	def parse(self, value):
		return value


class Nothing(Argument):
	def parse(self, value):
		value = super(Nothing, self).parse(value)
		if not value is None:
			raise ArgumentParseError("Is not null.")
		return value


class UnescapedUnicodeString(Argument):
	"""
	Used for unicodes stings which will not be escaped.
	"""
	pass


class UnicodeString(UnescapedUnicodeString):
	"""
	Used for unicodes stings which will be escaped, and wrapped in 'simple quotes'
	"""
	def parse(self, value):
		value = super(UnicodeString, self).parse(value)
		value = escape(value)
		if not isinstance(value, encoding.text_type):
			raise ArgumentParseError("Not a string.")
		return value





class Peer(UnescapedUnicodeString):
	def parse(self, value):
		value = super(Peer, self).parse(value)
		if " " in value:
			raise ArgumentParseError("Space in peer.")
		return value


class Chat(Peer):
	def parse(self, value):
		return super(Chat, self).parse(value)


class User(Peer):
	def parse(self, value):
		return super(User, self).parse(value)


class SecretChat(Peer):
	def parse(self, value):
		return super(SecretChat, self).parse(value)


class Number(Argument):
	def parse(self, value):
		super(Number, self).parse(value)
		if isinstance(encoding.native_type, encoding.text_type):
			return int(value)
		if not isinstance(value, (int, encoding.long_int)):
			raise ArgumentParseError("Not a int/long")
		return value




class Double(Argument):
	def parse(self, value):
		value = super(Double, self).parse(value)
		if not isinstance(value, float):
			raise ArgumentParseError("Not a float.")
		return value

class NonNegativeNumber(Number):
	def parse(self, value):
		value = super(NonNegativeNumber, self).parse(value)
		if value < 0:
			raise ArgumentParseError("Number smaller than 0.")
		return value


class PositiveNumber(NonNegativeNumber):
	def parse(self, value):
		value = super(PositiveNumber, self).parse(value)
		if value <= 0:
			raise ArgumentParseError("Number must be bigger than 0.")
		return value


class File(UnicodeString):
	def parse(self, value):
		if not path.isfile(encoding.native_type(value)):
			raise ArgumentParseError("File path \"{path}\" not valid.".format(path=value))
		value = super(File, self).parse(value)
		return value


class MsgId(PositiveNumber):
	def parse(self, value):
		return super(MsgId, self).parse(value)


def validate_input(function_name, arguments, arguments_types):
	logger.warn("validate_input() is deprecated!")
	raise NotImplementedError()

	if (len(arguments) != len(arguments_types)):
		raise ValueError("Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(function_name=function_name, expected_number=len(arguments_types), given_number=len(args)))
	i = 0
	new_args = []
	for arg in arguments:
		func_type = arguments_types[i]
		# arg is the given one, which should be func_type.
		if not func_type(arg):
			raise ValueError("Error in function {function_name}: parameter {number} is not type {type}.".format(function_name=function_name, number=i, type=func_type.__name__))
		if func_type == UnicodeString:
			new_args.append(encoding.to_unicode(escape(arg)))
		else:
			new_args.append(encoding.to_unicode(str(arg)))
		i += 1
	# end for
	return new_args