# -*- coding: utf-8 -*-
from collections import deque
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
from socket import error as socket_error
from errno import ECONNABORTED, EADDRINUSE


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
	_queue = deque()
	_new_messages = threading.Semaphore(0)
	_queue_access = threading.Lock()
	def __init__(self, host="localhost", port=4458, append_json=False):
		"""
		:param append_json: if the dict should contain the original json.
		"""
		self.host = host
		self.port = port
		self.append_json = append_json
	def start(self):
		receiver_thread = threading.Thread(target=self._receiver, args=())
		receiver_thread.daemon = True  # exit if script reaches end.
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
		print("Starting server on %s:%s" % (str(self.host), str(self.port)))
		while not self.QUIT:
			if self.s:
				self.s.close()
			del self.s
			###
			self.s = socket.socket()
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.settimeout(None) # enable blocking until we get a connention
			###
			failed = True
			count = 0
			while failed and not self.QUIT:
				try:
					self.s.bind((self.host, self.port))
				except socket_error as err:
					if err.errno == EADDRINUSE:
						print("Port assignment Failed. Address already in use. (Retring in 1 second.)")
						time.sleep(1)
						count = 1
						continue
					raise err
				else:
					failed = False
					if count == 1:
						print("Did Bind successfully.")
			###
			if self.QUIT:
				continue
			###
			self.s.listen(1) # allow 1 connection.
			###
			if self.QUIT:
				continue
			try:
				conn, addr = self.s.accept()
			except socket_error as err:
				if err.errno == ECONNABORTED and self.QUIT:
					continue
				raise
			####
			if self.QUIT:
				continue
			try:
				buffer = u("")
				result = "-NO DATA-"
				while not len(result) <= 0 and not self.QUIT:
					result = u(conn.recv(SOCKET_SIZE))
					buffer += result
				if self.QUIT:
					continue
				# print("Got result: >%s<" % buffer) # TODO remove.
				if (len(buffer) > 0 and buffer.strip() != ""):
					try:
						json_dict = json.loads(buffer)
						message = DictObject.objectify(json_dict)
						if self.append_json:
							message.merge_dict({u("json"): buffer})
					except ValueError as e:
						message = DictObject.objectify({u("error"):u(str(e)), u("json"): buffer})

					with self._queue_access:
						self._queue.append(message)
					self._new_messages.release()
			finally:
				if self.s:
					self.s.close()
		# end while not self.QUIT
		if self.s:
			self.s.close()
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
				with self._queue_access:
					msg = self._queue.popleft() #pop oldest item
				function.send(msg)
		except GeneratorExit:
			pass
		except KeyboardInterrupt:
			raise StopIteration
	#end def
#end class

