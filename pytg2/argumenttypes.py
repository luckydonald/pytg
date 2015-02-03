__author__ = 'luckydonald'
from . import encoding

def none(value):
	if value == None:
		return True
	return False

def peer(value):
	if not unicode_string(value):
		return False
	if " " in value:
		return False
	return True

def chat(value):
	if not peer(value):
		return False
	return True

def user(value):
	return peer(value)

def secret_chat(value):
	return peer(value)

def unicode_string(value):
	return isinstance(value, encoding.text_type)

def unescaped_unicode_string(value):
	"""
	Used for unicodes stings which will not be escaped.
	"""
	return isinstance(value, encoding.text_type)

def number(value):
	return isinstance(value, (int,long))

def double(value):
	return isinstance(value, float)

def positive_number(value):
	if number(value):
		if value > 0:
			return True
	return False

def nonnegative_number(value):
	if number(value):
		if value >= 0:
			return True
	return False

def msg_id(value):
	if unicode_string(value):
		try:
			int_val = int(value)
			return positive_number(int_val)
		except:
			return False
	return positive_number()

def optional():
	return True