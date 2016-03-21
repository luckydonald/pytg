# -*- coding: utf-8 -*-
from DictObject import DictObjectList, DictObject
from luckydonaldUtils import encoding
from luckydonaldUtils.encoding import to_unicode as u
import logging

from os import path

from .fix_msg_array import fix_peer
from .exceptions import IllegalResponseException, NoResponse, FailException

__author__ = 'luckydonald'
__all__ = ["raw", "nothing", "something", "anything", "success_fail", "response_fails", "ResultParser", "List", "OnlineEvent"]
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


def success_fail(json, need_success=True):
    """
    Will return True if json.result == "SUCCESS".
    If json.result was not found, and need_success is set to True, a IllegalResponseException is raised.
    If json.result was not found, and need_success is set to False, it will return the original json.

    :param json: The input to check.
    :type  json: DictObject
    :keyword need_success: if true it will raise a IllegalResponseException if json.result is not found.
    :type    need_success: bool
    :returns: True if json.result == "SUCCESS", or the given json if json.result is not found.
    :rtype: bool | DictObject
    """
    if not need_success and not "result" in json:
        return json
    if json.result == u("SUCCESS"):
        return True
    if json.result == u("FAIL"):
        raise FailException(json.error_code, json.error)
    raise IllegalResponseException("Found: {}".format(json))
# end def


def downloaded_file(json, check_files=True):
    """
    Checks that the download was successful.

    :param json: The json from the cli.
    :type  json: DictObject

    :keyword check_files: If it should verify the file path.
    :type    check_files: bool

    :return: The file path.
    :rtype:  str
    """
    if "event" not in json or not json.event:
        raise IllegalResponseException("Has no valid event attribute.")
    if json.event != u("download"):
        raise IllegalResponseException("Download event should be 'download'.")
    if "result" not in json or not json.result:
        raise IllegalResponseException("Has no valid result attribute.")
    if check_files and not path.isfile(encoding.native_type(json.result)):
        raise IllegalResponseException("File path \"{path}\" not valid.".format(path=json.result))
    else:
        return json.result


def response_fails(exception=None, *args):
    if len(args) > 0:
        logger.warn("response_fails: args: {}", args)
    if exception is None:
        raise IllegalResponseException("Did not throw timeout exception.")
    if isinstance(exception, NoResponse):
        return None if len(args) == 0 else args[0] if len(args) == 1 else args
    raise IllegalResponseException("Wrong exception: {exc}".format(exc=str(type(exception))))


class ResultParser(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Yo. Somebody probably forgot to write some code.")


class List(ResultParser):
    def __call__(self, json):
        if isinstance(json, DictObjectList):
            return json
        else:
            raise IllegalResponseException("Not a list: {json}".format(json=str(json)))


class OnlineEvent(ResultParser):
    def __call__(self, json):
        """
        :type json: DictObject
        """
        if not isinstance(json, DictObject):
            raise IllegalResponseException("Not a dict: {json}".format(json=str(json)))
        assert isinstance(json, DictObject)
        success_fail(json, need_success=False)
        _check_if_has(json, "when", str)
        _check_if_has(json, "user", DictObject)
        json["user"] = fix_peer(json["user"])
        return json


def _check_if_has(json, key, expected_type=None):
    if key not in json:
        raise IllegalResponseException("Could not find key \"{key}\" in dict: {json}".format(key=key, json=str(json)))
    if type is not None:
        if not isinstance(json[key], expected_type):
            raise IllegalResponseException("Key \"{key}\" is not type {type_expected}, but is type {type_is}: {json}"
                                           .format(key=key, type_expected=str(expected_type), type_is=type(json[key]),
                                                   json=str(json)))

