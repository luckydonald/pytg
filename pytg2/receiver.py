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
from .encoding import to_native as n
from socket import error as socket_error
from errno import ECONNABORTED, EADDRINUSE, EINTR
import logging

logger = logging.getLogger(__name__)

SOCKET_SIZE = 1 << 25
BLOCK_SIZE = 256
RESPONSE_ERROR = b("ERR")
RESPONSE_ACKNOWLEDGED = b("ACK")
EMPTY_UNICODE_STRING = u("") # So we don't call it every time in the if header.
EMPTY_RAW_BYTE = b("") # So we don't call it every time in the if header.
_ANSWER_SYNTAX = b("LENGTH ")
_LINE_BREAK = b("\n")

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
		logger.info("Starting server on %s:%s" % (str(self.host), str(self.port)))
		while not self._do_quit:
			# close socket, if existent. Just beeing sure.
			if self.s:
				self.s.close()
			del self.s
			### open new socket
			self.s = socket.socket()
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.settimeout(None) # enable blocking until we get a connention
			### binding address.
			failed = True
			count = 0
			while failed and not self._do_quit:
				try:
					self.s.bind((self.host, self.port))
				except socket_error as err:
					if err.errno == EADDRINUSE:
						logger.error("Port assignment Failed. Address already in use. (Retring in 1 second.)")
						time.sleep(1)
						count = 1
						continue
					raise err
				else:
					failed = False
					if count == 1:
						logger.info("Did Bind successfully.")
			if self._do_quit:
				continue

			### start listening

			self.s.listen(1) # allow 1 connection.
			if self._do_quit:
				continue
				
			try:
				conn, addr = self.s.accept()
			except socket_error as err:
				if err.errno == ECONNABORTED and self._do_quit:
					continue
				raise



			success = True
			completed = -1 # -1 = answer size yet unknown, >0 = got remaining answer size
			buffer = EMPTY_RAW_BYTE
			try:
				while completed != 0:
					while 1: #retry recv(1) if CTRL+C'd
						try:
							answer = conn.recv(1)
							break
						except socket_error as err:
							if err.errno != EINTR: # not CTRL+C'd
								raise
					buffer += answer
					if completed < -1 and buffer[:len(_ANSWER_SYNTAX)] != _ANSWER_SYNTAX[:len(buffer)]:
						self._send_acknowledged(False, conn)
						raise ArithmeticError("Server response does not fit.")
					if completed <= -1 and buffer.startswith(_ANSWER_SYNTAX) and buffer.endswith(_LINE_BREAK):
						try:
							completed = int(n(buffer[ len(_ANSWER_SYNTAX)-1 : -len(_LINE_BREAK) ]))+1 #TODO regex for numbers?
						except:
							self._send_acknowledged(False, conn) # Length failed.
							self.s.close()
							raise
						self._send_acknowledged(True, conn)  #TODO: fail check?
						logger.debug("Loading message with length {}.".format(completed))
						buffer = EMPTY_RAW_BYTE
					completed -= 1
				text = n(buffer)
				if len(text) > 0 and text.strip() != EMPTY_UNICODE_STRING:
						if self._do_quit:
							continue
						try:
							logger.debug("Received Message: \"{str}\"".format(str=text))
							json_dict = json.loads(text)
							message = DictObject.objectify(json_dict)
							if self.append_json:
								message.merge_dict({u("json"): text})
							with self._queue_access:
								self._queue.append(message)
								self._new_messages.release()
						except ValueError as e:
							# DictObject.objectify({u("error"): u(str(e)), u("json"): buffer})
							logger.error("Received message could not be parsed.".format())
							raise
			except Exception as err:
				logger.exception("Exception while receiving Message. Got so far: >%s<\n%s" % (n(buffer),str(err))) #TODO remove me
				success = False
				raise
			finally:
				if not self._do_quit:  # open socket is supposed to exist.
					self._send_acknowledged(success, conn)
					self.s.close()
			# end try/except/finally
		# end while(not self._do_quit)
		if self.s:
			self.s.close() # if the while exits because of _do_quit
	# end def

	def _send_acknowledged(self,success, connection):
		logger.info("Sending acknowledged {bool}".format(bool=success))
		if connection:
			old_timeout = connection.gettimeout()
			self.s.settimeout(10)
			try:
				if success:
					connection.send(RESPONSE_ACKNOWLEDGED) # 'ACK'
				else:
					connection.send(RESPONSE_ERROR) # 'ERR'
			except socket.timeout as e:
				#logger.warn("Acknowledge send timeout")
				pass
			connection.settimeout(old_timeout)
			

	@coroutine
	def message(self, function):
		if not isinstance(function, GeneratorType):
			raise TypeError('Target must be GeneratorType')
		try:
			while not self._do_quit:
				self._new_messages.acquire() # waits until at least 1 message is in the queue.
				with self._queue_access:
					logger.debug('Messages waiting in queue: %d', len(self._queue))
					message = self._queue.popleft() #pop oldest item
				function.send(message)
		except GeneratorExit:
			pass
		except KeyboardInterrupt:
			raise StopIteration
	#end def
#end class

