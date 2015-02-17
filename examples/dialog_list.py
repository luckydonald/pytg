__author__ = 'luckydonald'

if __name__ == '__main__':
	# Test.
	from pytg2.sender import Sender
	x = Sender("127.0.0.1", 1337)
	res = x.get_dialog_list()
	print("Got: >%s<" % res)
	res = x.get_dialog_list()
	print("Got: >%s<" % res)




def ____():
	"""
	Test only.
	>>> x = Sender("127.0.0.1", 1337)
	>>> x.msg("luckydonald",5)
	SUCCESS
	>>> x.send_typing("luckydonald",9)
	SUCCESS
	>>> x.send_typing("luckydonald",900)
	FAIL

	In case there is no such function, use
	>>> x.raw(u"quit")
	print("Got: >%s<" % res)
	"""