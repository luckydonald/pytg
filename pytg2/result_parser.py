__author__ = 'luckydonald'
from .encoding import to_unicode as u
from .encoding import to_native as n


class IllegalResponseException(Exception):
	pass


def nothing(value):
	if value and len(value) > 1:
		raise IllegalResponseException("Should return nothing.")
	return True


def something(value):
	if not (value and len(value) > 1):
		raise IllegalResponseException("Should return something.")


def success_fail(value):
	if value == u("SUCCESS"):
		return True
	if value == u("FAIL"):
		return False
	raise IllegalResponseException("Found \"%s\"" % n(value))
