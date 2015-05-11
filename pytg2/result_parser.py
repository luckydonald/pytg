__author__ = 'luckydonald'
from .encoding import to_unicode as u
from .encoding import to_native as n
from .exceptions import IllegalResponseException, NoResponse


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

def success_fail(value):
	if value == u("SUCCESS"):
		return True
	if value == u("FAIL"):
		return False
	raise IllegalResponseException("Found \"%s\"" % n(value))

def response_fails(exception=None):
	if exception is None:
		raise IllegalResponseException("Did not throw timeout exception.")
	if isinstance(exception, NoResponse):
		return
	raise IllegalResponseException("Wrong exception: {exc}".format(exc=str(type(exception))))
