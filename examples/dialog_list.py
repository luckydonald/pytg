__author__ = 'luckydonald'

def main():
	from pytg2.sender import Sender
	x = Sender("127.0.0.1", 1337)
	res = x.get_dialog_list()
	print("Got: >%s<" % res)



if __name__ == '__main__':
	main()