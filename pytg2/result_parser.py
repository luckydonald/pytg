__author__ = 'luckydonald'
from .encoding import to_unicode as u

class IllegalResponseException(Exception):
	pass

def success_fail(value):
	if value == u("SUCCESS"):
		return True
	if value == u("FAIL"):
		return False
	raise IllegalResponseException(value)
