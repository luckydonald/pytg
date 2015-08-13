# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from luckydonaldUtils import encoding
from .utils import escape  # validate_input
from .exceptions import ArgumentParseError
from os import path # file checking.
import logging
logger = logging.getLogger(__name__)


class Argument(object):
	type="unknown-argument-type"
	def __init__(self, name, optional=False, multible=False, default=None):
		self.name = name
		self.optional = optional
		self.multible = multible
		self.default = default

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
	type="None"
	def parse(self, value):
		value = super(Nothing, self).parse(value)
		if not value is None:
			raise ArgumentParseError("Is not null.")
		return value


class UnescapedUnicodeString(Argument):
	"""
	Used for unicodes stings which will not be escaped.
	"""
	type="str"
	pass


class UnicodeString(UnescapedUnicodeString):
	"""
	Used for unicodes stings which will be escaped, and wrapped in 'simple quotes'
	"""
	type="str"
	def parse(self, value):
		value = super(UnicodeString, self).parse(value)
		value = escape(value)
		if not isinstance(value, encoding.text_type):
			raise ArgumentParseError("Not a string.")
		return value





class Peer(UnescapedUnicodeString):
	type="str"
	def parse(self, value):
		value = super(Peer, self).parse(value)
		if " " in value:
			raise ArgumentParseError("Space in peer.")
		return value


class Chat(Peer):
	type="str"
	def parse(self, value):
		return super(Chat, self).parse(value)


class User(Peer):
	type="str"
	def parse(self, value):
		return super(User, self).parse(value)


class SecretChat(Peer):
	type="str"
	def parse(self, value):
		return super(SecretChat, self).parse(value)


class Number(Argument):
	type="int"
	def parse(self, value):
		super(Number, self).parse(value)
		if isinstance(encoding.native_type, encoding.text_type):
			return int(value)
		if not isinstance(value, (int, encoding.long_int)):
			raise ArgumentParseError("Not a int/long")
		return value




class Double(Argument):
	type="float"
	def parse(self, value):
		value = super(Double, self).parse(value)
		if not isinstance(value, float):
			raise ArgumentParseError("Not a float.")
		return value

class NonNegativeNumber(Number):
	type="int >= 0"
	def parse(self, value):
		value = super(NonNegativeNumber, self).parse(value)
		if value < 0:
			raise ArgumentParseError("Number smaller than 0.")
		return value


class PositiveNumber(NonNegativeNumber):
	type="int > 0"
	def parse(self, value):
		value = super(PositiveNumber, self).parse(value)
		if value <= 0:
			raise ArgumentParseError("Number must be bigger than 0.")
		return value


class File(UnicodeString):
	type="str"
	def parse(self, value):
		if not path.isfile(encoding.native_type(value)):
			raise ArgumentParseError("File path \"{path}\" not valid.".format(path=value))
		value = super(File, self).parse(value)
		return value


class MsgId(PositiveNumber):
	type="int"
	def parse(self, value):
		return super(MsgId, self).parse(value)