__author__ = 'luckydonald'
from .encoding import to_unicode as u
from .encoding import to_native as n
from .exceptions import IllegalResponseException, NoResponse
import logging

logger = logging.getLogger(__name__)

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
		return False
	raise IllegalResponseException("Found: {}".format(json))

def response_fails(exception=None, *args):
	if len(args) > 0:
		logger.warn("response_fails: args: {}",args)
	if exception is None:
		raise IllegalResponseException("Did not throw timeout exception.")
	if isinstance(exception, NoResponse):
		return
	raise IllegalResponseException("Wrong exception: {exc}".format(exc=str(type(exception))))