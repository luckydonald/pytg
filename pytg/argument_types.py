# -*- coding: utf-8 -*-

from luckydonaldUtils import encoding
from .utils import escape  # validate_input
from .exceptions import ArgumentParseError
from os import path  # file checking.
import logging, re

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)

USERNAME_REGEX = re.compile(
    "^@?(?P<username>(?:[a-z](?:[a-z0-9]|_(?!_)){3,}[a-z0-9])|(?:gif|vid|wiki|pic|bing|imdb|bold))$",
    # https://regex101.com/r/eV1oV1
    flags=re.IGNORECASE
)


class Argument(object):
    type = "unknown-argument-type"  # used when generating docstrings for sender.py's functions

    def __init__(self, name, optional=False, multible=False, default=None):
        self.name = name
        self.optional = optional
        self.multible = multible
        self.default = default

    def __str__(self):
        string = self.name
        if self.optional:
            string = "[" + string + "]"
        else:
            string = "<" + string + ">"
        if self.multible:
            string += "+"
        return string

    def parse(self, value):
        return value


class Nothing(Argument):
    type = "None"

    def parse(self, value):
        value = super(Nothing, self).parse(value)
        if not value is None:
            raise ArgumentParseError("Is not null.")
        return value


class UnescapedUnicodeString(Argument):
    """
    Used for unicodes stings which will not be escaped. (no need for escaping and 'simple quotes')
    """
    type = "str"
    pass


class UnicodeString(Argument):
    """
    Used for unicodes stings which will be escaped, and wrapped in 'simple quotes'
    """
    type = "str"

    def parse(self, value):
        value = super(UnicodeString, self).parse(value)
        value = escape(value)
        if not isinstance(value, encoding.text_type):
            raise ArgumentParseError("Not a string.")
        return value


class PermanentID(UnescapedUnicodeString):
    type = "str"

    def parse(self, value):
        if not isinstance(value, encoding.unicode_type):
            raise ArgumentParseError("Not a (unicode) string.")
        # TODO: Regex
        return value


class Peer(UnescapedUnicodeString):
    type = "str"

    def parse(self, value):
        value = super(Peer, self).parse(value)
        if " " in value:
            raise ArgumentParseError("Space in peer.")
        return value


class Username(UnicodeString):
    type = "str"

    def parse(self, value):
        if not USERNAME_REGEX.match(value):
            raise ArgumentParseError(
                "Username {username} did not match regex.".format(username=value)
            )  # See https://regex101.com/r/eV1oV1
        return value


class Chat(Peer):
    type = "str"

    def parse(self, value):
        return super(Chat, self).parse(value)


class User(Peer):
    type = "str"

    def parse(self, value):
        value = super(User, self).parse(value)
        return value


class SecretChat(Peer):
    type = "str"

    def parse(self, value):
        return super(SecretChat, self).parse(value)


class Channel(Peer):
    type = "str"

    def parse(self, value):
        return super(Peer, self).parse(value)


class Number(Argument):
    type = "int"

    def parse(self, value):
        super(Number, self).parse(value)
        if isinstance(encoding.native_type, encoding.text_type):
            return int(value)
        if not isinstance(value, (int, encoding.long_int)):
            raise ArgumentParseError("Not a int/long")
        return value


class Double(Argument):
    type = "float"

    def parse(self, value):
        value = super(Double, self).parse(value)
        if not isinstance(value, float):
            raise ArgumentParseError("Not a float.")
        return value


class NonNegativeNumber(Number):
    type = "int >= 0"

    def parse(self, value):
        value = super(NonNegativeNumber, self).parse(value)
        if value < 0:
            raise ArgumentParseError("Number smaller than 0.")
        return value


class PositiveNumber(NonNegativeNumber):
    type = "int > 0"

    def parse(self, value):
        value = super(PositiveNumber, self).parse(value)
        if value <= 0:
            raise ArgumentParseError("Number must be bigger than 0.")
        return value


class FilePath(UnicodeString):
    type = "str"

    def parse(self, value, check_files=True):
        """
            File argument.

            :param value: The file path.
            :type  value: str

            :keyword check_files: If it should verify the file path.
            :type    check_files: bool

            :return: Argument ready string.
            :rtype:  str
            """
        if not path.isfile(encoding.native_type(value)):
            raise ArgumentParseError("File path \"{path}\" not valid.".format(path=value))
        value = super(FilePath, self).parse(value)
        return value


class MsgId(PermanentID):
    type = "str"

    def parse(self, value):
        return super(MsgId, self).parse(value)
