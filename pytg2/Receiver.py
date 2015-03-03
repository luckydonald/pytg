# -*- coding: utf-8 -*-
from socket import SHUT_RDWR
import threading

__author__ = 'luckydonald'

import socket # connect to telegram cli.
import time # wait for retry
from DictObject import DictObject
import json
from .utils import coroutine, suppress_context
from types import GeneratorType
from . import encoding
from .encoding import to_unicode as u

SOCKET_SIZE = 1 << 25

class Receiver(object):
	"""
	Start telegram client somewhere.
	$ ./bin/telegram-cli -P 1337 -s 127.0.0.1:4458 -W
	Get a telegram
	>>> tg = Receiver()
	>>> tg.start()

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
		"""
		Shuts down the receivers server.
		No more messages will be received.
		"""
		self.QUIT = True
		if self.s:
			self.s.settimeout(0)
		#if self.s.c:
			#self.s.shutdown(SHUT_RDWR)
		if self.s:
			self.s.close()
		self._new_messages.release()



	def _receiver(self):
		"""
		Server.
		"""
		self.s = None
		print("Started server.")
		while not self.QUIT:
			if self.s:
				self.s.close()
			del self.s
			self.s = socket.socket()
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.settimeout(None) # enable blocking until we get a connention
			failed = True
			while failed:
				if self.QUIT:
					break
				try:
					self.s.bind((self.host, self.port))
				except Exception as err:
					if self.QUIT:
						break
					print(err)
					print("Port assignment Failed. Retring in 1 second.")
					time.sleep(1)
				else:
					failed = False
			if self.QUIT:
				 continue
			self.s.listen(1) # allow 1 connection.
			if self.QUIT:
				continue
			conn, addr = self.s.accept()
			if self.QUIT:
				continue
			try:
				buffer = u("")
				result = "-NO DATA-"
				while not len(result) <= 0:
					result = u(conn.recv(SOCKET_SIZE))
					if self.QUIT:
						continue
					buffer += result
				print("Got result: >%s<" % buffer) # TODO remove.
				if (len(buffer) > 0 and buffer.strip() != ""):
					message = DictObject.objectify(json.loads(buffer))
					self._queue.append(message)
					self._new_messages.release()
			except ValueError: #json
				raise
			finally:
				if self.s:
					self.s.close()
		# end while not self.QUIT
	# end def

	@coroutine
	def message(self, function):
		if type(function) is not GeneratorType:
			raise TypeError('target must be GeneratorType')
		try:
			while not self.QUIT:
				self._new_messages.acquire() # waits until at least 1 message is in the queue.
				if self.QUIT:
					continue
				function.send(self._queue.pop())
		except GeneratorExit:
			pass
	#end def
#end class

