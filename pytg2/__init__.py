# -*- coding: utf-8 -*-
import threading

__author__ = 'luckydonald'

import socket # connect to telegram cli.
import time # wait for retry
from DictObject import DictObject
import json
from utils import coroutine
from types import GeneratorType


SOCKET_SIZE = 1 << 25

class Telegram(object):
	"""
	Get a telegram
	>>> tg = Telegram()
	>>> tg.start();

	"""
	QUIT = False
	_queue = []
	_messages = threading.Semaphore(0)
	def __init__(self):
		self.host = "127.0.0.1"
		self.port = 4458
	def start(self):
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = False #don't exit if script reaches end. Use self.QUIT
		thread.start()

	def run(self):
		"""
		Server.
		"""
		s = None;
		print("Started server.")
		while not self.QUIT:
			if s:
				s.close()
			del s;
			s = socket.socket()
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			failed = True
			while failed:
				try:
					s.bind(((self.host), self.port))
				except Exception as err:
					print(err)
					print("Port assignment Failed. Retring in 1 second.")
					time.sleep(1)
				else:
					failed = False
					print("Successful bound to port.")
			s.listen(1) # allow 1 connection.
			print("Listening!")
			conn, addr = s.accept()
			print("Got connection %s , %s" %(str(conn), str(addr)))
			try:
				buffer = ""
				result = "-NO DATA-"
				while not len(result) == 0:
					result = conn.recv(SOCKET_SIZE).decode('utf-8')
					print("Got something: " + str(result))
					buffer += result
				print("Got result: " + buffer)
				message = DictObject.objectify(json.loads(buffer))
				self._queue.append(message)
				self._messages.release()
			finally:
				s.close()
		# end while not self.QUIT
	# end def
	def message(self, target):
		if type(target) is not GeneratorType:
			raise TypeError('target must be GeneratorType')
		try:
			while not self.QUIT:
				self._messages.acquire()
				target.send(self._queue.pop())
		except GeneratorExit:
			pass
	#end def
#end class

#@coroutine
def dialog_list(target):
	"""
	Get the dialog list.
	:param target:
	:raise TypeError:
	"""
	#if type(target) is not GeneratorType:
	#	raise TypeError('target must be GeneratorType')

@coroutine
def test(tg):
	while True:
		msg = (yield)
		print("MSG: "+ str(msg))
		time.sleep(10)

if __name__ == '__main__':
	tg = Telegram() #get a Telegram Connector instance
	tg.start() #start the Connector.
	tg.message(test(tg)) # add "test" function as listeners. You can supply arguments here (like tg).
