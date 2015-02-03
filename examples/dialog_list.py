__author__ = 'luckydonald'

if __name__ == '__main__':
#def ____():
	"""
	Test only.
	>>> x = Sender("127.0.0.1", 1337)
	>>> x.msg("luckydonald",5)
	SUCCESS
	>>> x.send_typing("luckydonald",9)
	SUCCESS
	>>> x.send_typing("luckydonald",900)
	FAIL

	"""
	# Test.
	from pytg2.sender import Sender
	x = Sender("127.0.0.1", 1337)  # 9034
	#res = x.msg("luckydonald",5)
	# res = x.mark_read("luckydonald")
	#print("Got: %s" % res)
	res = x.get_dialog_list()
	print("Got: >%s<" % res)
	res = x.get_dialog_list()
	print("Got: >%s<" % res)