# -*- coding: utf-8 -*-
from DictObject import DictObjectList
from luckydonaldUtils.encoding import to_unicode as u
import logging

from .fix_msg_array import fix_peer
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


class OnlineEvent(ResultParser):
    def __call__(self, json):
        if not isinstance(json, dict):
            raise IllegalResponseException("Not a dict: {json}".format(json=str(json)))
        _check_if_has(json, "when", str)
        _check_if_has(json, "user", dict)
        json["user"] = fix_peer(json["user"])
        return json


def _check_if_has(json, key, expected_type=None):
    if key not in json:
        raise IllegalResponseException("Cloud not find key \"{key}\" in dict: {json}".format(key=key, json=str(json)))
    if type is not None:
        if not isinstance(json[key], expected_type):
            raise IllegalResponseException("Key \"{key}\" is not type {type_expected}, but is type {type_is}: {json}"
                                           .format(key=key, type_expected=str(expected_type), type_is=type(json[key]),
                                                   json=str(json)))

