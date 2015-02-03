__author__ = 'luckydonald'
from pytg2.receiver import Receiver
from pytg2.utils import coroutine

@coroutine
def example_function(tg):
	try:
		while True:
			msg = (yield)
			print('Message "{text}", full dump: {array}'.format(text=str( msg['text'] ), array=str( msg )))
	except KeyboardInterrupt:
		print("Exiting")

if __name__ == '__main__':
	tg = Receiver(port=4458) #get a Receiver Connector instance
	tg.start() #start the Connector.
	tg.message(example_function(tg)) # add "example_function" function as listeners. You can supply arguments here (like tg).
	# continues here, after exiting while loop in example_function()
	tg.stop()
