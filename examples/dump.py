__author__ = 'luckydonald'
from pytg2 import Telegram
from pytg2.utils import coroutine

@coroutine
def test(tg):
	while True:
		msg = (yield)
		print('Message "{text}", full dump: {array}'.format(text=str( msg['text'] ), array=str( msg )))

if __name__ == '__main__':
	tg = Telegram() #get a Telegram Connector instance
	tg.start() #start the Connector.
	tg.message(test(tg)) # add "test" function as listeners. You can supply arguments here (like tg).
