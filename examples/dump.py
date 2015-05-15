# -*- coding: utf-8 -*-
__author__ = 'luckydonald'
from pytg2.receiver import Receiver
from pytg2.utils import coroutine

@coroutine
def example_function(receiver):
	try:
		while True:
			msg = (yield)
			print('Full dump: {array}'.format(array=str( msg )))
	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")

if __name__ == '__main__':
	receiver = Receiver(port=4458) #get a Receiver Connector instance
	receiver.start() #start the Connector.
	receiver.message(example_function(receiver)) # add "example_function" function as listeners. You can supply arguments here (like receiver).
	# continues here, after exiting while loop in example_function()
	receiver.stop()
