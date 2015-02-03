__author__ = 'luckydonald'

def suppress_context(exc):
	exc.__context__ = None
	return exc


def escape(string):
	return string.replace("'","\\'").join(["'","'"])


def coroutine(func):
	"""
	Skips to the first yield when the generator is created.
	Used as decorator, @coroutine
	:param func: function (generator) with yield.
	:return: generator
	"""

	def start(*args, **kwargs):
		cr = func(*args, **kwargs)
		try:
			next(cr)
		except NameError: # not defined, python 2
			cr.next()
		return cr

	return start