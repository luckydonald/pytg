# -*- coding: utf-8 -*-
from DictObject import DictObjectList
from luckydonaldUtils.encoding import to_unicode as u
import logging

from .exceptions import IllegalResponseException, NoResponse

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)


def raw(value):
    return value


def nothing(value):
    if value:
        raise IllegalResponseException("Should return nothing.")
    return True


def something(value):
    if not (value and len(value) > 1):
        raise IllegalResponseException("Should return something.")
    return value


def anything(value):
    return value


def success_fail(json):
    if json.result == u("SUCCESS"):
        return True
    if json.result == u("FAIL"):
        return json
    raise IllegalResponseException("Found: {}".format(json))


def response_fails(exception=None, *args):
    if len(args) > 0:
        logger.warn("response_fails: args: {}", args)
    if exception is None:
        raise IllegalResponseException("Did not throw timeout exception.")
    if isinstance(exception, NoResponse):
        return None if len(args) == 0 else args[0] if len(args) == 1 else args
    raise IllegalResponseException("Wrong exception: {exc}".format(exc=str(type(exception))))


class ResultParser(object):
    pass


class List(ResultParser):
    def __call__(self, json):
        if isinstance(json, DictObjectList):
            return json
        else:
            raise IllegalResponseException("Not a list: {json}".format(json=str(json)))
