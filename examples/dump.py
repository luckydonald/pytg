__author__ = 'luckydonald'
from pytg2 import Telegram
from pytg2.utils import coroutine

@coroutine
def example_function(tg):
	try:
		while True:
			msg = (yield)
			print('Message "{text}", full dump: {array}'.format(text=str( msg['text'] ), array=str( msg )))
			if msg['out'] == False:
				tg._do_send("msg chat#3921114 Ping")
	except KeyboardInterrupt:
		print("Exiting")

if __name__ == '__main__':
	tg = Telegram(port_out=9034) #get a Telegram Connector instance
	tg.start() #start the Connector.
	tg.message(example_function(tg)) # add "example_function" function as listeners. You can supply arguments here (like tg).
	# continues here, after exiting while loop in example_function()
	tg.stop()
