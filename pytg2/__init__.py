# -*- coding: utf-8 -*-
import threading

__author__ = 'luckydonald'

import socket # connect to telegram cli.
import time # wait for retry
from DictObject import DictObject
import json
from .utils import coroutine, suppress_context
from types import GeneratorType
from . import encoding
from .encoding import to_unicode

SOCKET_SIZE = 1 << 25

class Receiver(object):
	"""
	Start telegram client somewhere.
	$ ./bin/telegram-cli -P 1337 -s 127.0.0.1:4458 -W
	Get a telegram
	>>> tg = Receiver()
	>>> tg.start();

	"""
	QUIT = False
	_queue = []
	_new_messages = threading.Semaphore(0)
	def __init__(self, host="localhost", port=4458):
		self.host = host
		self.port = port
	def start(self):
		receiver_thread = threading.Thread(target=self._receiver, args=())
		receiver_thread.daemon = False  # don't exit if script reaches end. Use self.QUIT
		receiver_thread.start()

	def stop(self):
		self.QUIT = True

	def _receiver(self):
		"""
		Server.
		"""
		s = None
		print("Started server.")
		while not self.QUIT:
			if s:
				s.close()
			del s
			s = socket.socket()
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			failed = True
			while failed:
				try:
					s.bind((self.host, self.port))
				except Exception as err:
					print(err)
					print("Port assignment Failed. Retring in 1 second.")
					time.sleep(1)
				else:
					failed = False
			s.listen(1) # allow 1 connection.
			conn, addr = s.accept()
			try:
				buffer = ""
				result = "-NO DATA-"
				while not len(result) <= 0:
					result = to_unicode(conn.recv(SOCKET_SIZE))
					buffer += result
				print("Got result: >%s<" % buffer) # TODO remove.
				if (buffer != "" and  len(buffer) > 0 and buffer.strip() != ""):
					message = DictObject.objectify(json.loads(buffer))
					self._queue.append(message)
					self._new_messages.release()
			finally:
				s.close()
		# end while not self.QUIT
	# end def

	def message(self, function):
		if type(function) is not GeneratorType:
			raise TypeError('target must be GeneratorType')
		try:
			while not self.QUIT:
				self._new_messages.acquire() # waits until at least 1 message is in the queue.
				function.send(self._queue.pop())
		except GeneratorExit:
			pass
	#end def
#end class

