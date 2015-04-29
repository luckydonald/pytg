# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from collections import deque
from socket import SHUT_RDWR
import threading
import socket # connect to telegram cli.
import time # wait for retry
from DictObject import DictObject
import json
from .utils import coroutine, suppress_context
from types import GeneratorType
from . import encoding
from .encoding import to_unicode as u
from .encoding import to_binary as b
from socket import error as socket_error
from errno import ECONNABORTED, EADDRINUSE


SOCKET_SIZE = 1 << 25
BLOCK_SIZE = 256
RESPONSE_ERROR = b("ERR")
RESPONSE_ACKNOWLEDGED = b("ACK")
EMPTY_UNICODE_STRING = u("") # So we don't call it every time in the if header.


class Receiver(object):
	"""
	Start telegram client somewhere.
	$ ./bin/telegram-cli -P 1337 -s 127.0.0.1:4458 -W
	Get a telegram
	>>> tg = Receiver()
	>>> tg.start()

	"""
	_do_quit = False
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
		self._do_quit = True
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
		while not self._do_quit:
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
			while failed and not self._do_quit:
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
			if self._do_quit:
				continue
			###
			self.s.listen(1) # allow 1 connection.
			###
			if self._do_quit:
				continue
			try:
				conn, addr = self.s.accept()
			except socket_error as err:
				if err.errno == ECONNABORTED and self._do_quit:
					continue
				raise
			try:
				# buffer = EMPTY_UNICODE_STRING
				result = "-NO DATA-"  # so len(result) is > 0
				result_buffer = b("")
				while len(result) > 0 and not self._do_quit:
					result = conn.recv(BLOCK_SIZE)
					result_buffer += result
					#print("resultpart: %s" % u(result))
				buffer = u(result_buffer)
				print("Got result: >%s<" % buffer) # TODO remove.
				if len(buffer) > 0 and buffer.strip() != EMPTY_UNICODE_STRING:
					if self._do_quit:
						continue
					try:
						json_dict = json.loads(buffer)
						message = DictObject.objectify(json_dict)
						if self.append_json:
							message.merge_dict({u("json"): buffer})
						with self._queue_access:
							self._queue.append(buffer)
							self._new_messages.release()
					except ValueError as e:
						# DictObject.objectify({u("error"): u(str(e)), u("json"): buffer})
						raise

			except Exception as err:
				print (err)
				if self.s:
					self.s.sendall(RESPONSE_ERROR) # 'ERR'
			else:
				if self.s:
					self.s.sendall(RESPONSE_ACKNOWLEDGED) # 'ACK'
			finally:
				if self.s:
					self.s.close()
		# end while not self._do_quit
		if self.s:
			self.s.close()
	# end def

	@coroutine
	def message(self, function):
		if not isinstance(function, GeneratorType):
			raise TypeError('Target must be GeneratorType')
		try:
			while not self._do_quit:
				self._new_messages.acquire() # waits until at least 1 message is in the queue.
				with self._queue_access:
					print('Messages Waiting: ', len(self._queue))
					message = self._queue.popleft() #pop oldest item
				function.send(message)
		except GeneratorExit:
			pass
		except KeyboardInterrupt:
			raise StopIteration
	#end def
#end class

