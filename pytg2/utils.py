__author__ = 'luckydonald'

def suppress_context(exc):
	exc.__context__ = None
	return exc


def escape(string):
	for i in range(0,7):
		string = string.replace(["\\","\n","\r","\t","\b","\a","'"][i], ["\\\\","\\n","\\r","\\t","\\b","\\a","\\'"][i])
	return string.join(["'","'"])


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
			except NameError: # not defined, python 2
				cr.next()
			return cr
		except StopIteration:
			return

	return start