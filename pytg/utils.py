# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

CHARS_UNESCAPED = ["\\", "\n", "\r", "\t", "\b", "\a", "'"]
CHARS_ESCAPED = ["\\\\", "\\n", "\\r", "\\t", "\\b", "\\a", "\\'"]


def suppress_context(exc):
    exc.__context__ = None
    return exc


def escape(string):
    for i in range(0, 7):
        string = string.replace(CHARS_UNESCAPED[i], CHARS_ESCAPED[i])
    return string.join(["'", "'"])  # wrap with single quotes.


def coroutine(func):
    """
    Skips to the first yield when the generator is created.
    Used as decorator, @coroutine
    :param func: function (generator) with yield.
    :return: generator
    """

    def start(*args, **kwargs):
        try:
            cr = func(*args, **kwargs)
            try:
                next(cr)
            except NameError:  # not defined, python 2
                cr.next()
            return cr
        except StopIteration:
            return
        except KeyboardInterrupt:
            raise StopIteration

    return start
