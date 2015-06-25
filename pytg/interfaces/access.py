# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)
import threading
from collections import deque
from types import GeneratorType

from ..utils import coroutine

class PublicInterface(object):
	def __init__(self, interface):
		"""
		:param interface: The Telegram interface to use.
		:type  interface: MessageConstructorSuperclass
		"""
		super(PublicInterface, self).__init__()
		if not isinstance(interface, MessageConstructorSuperclass):
			raise TypeError("Parameter interface is not type MessageConstructorSuperclass, but type {type}".format(
				type=type(interface)))
		self.interface = interface
		self._do_quit = False
		self._queue = deque()
		self._new_messages = threading.Semaphore(0)
		self._queue_access = threading.Lock()

	def _add_message(self, raw_event):
		"""
		Appends a message to the message queue.

		:type text: builtins.str
		:return:
		"""
		json_dict = {}
		logger.debug("Received Message: \"{str}\"".format(str=text))
		with self._queue_access:
			self._queue.append(raw_event) # change me!
			self._new_messages.release()

	def queued_messages(self):
		"""
		Informs how many messages are still in the queue, waiting to be processed.

		:return: integer, the messages currently in queue.
		:rtype: int
		"""
		with self._queue_access:
			return len(self._queue)

	@coroutine
	def for_each_event(self, function):
		if not isinstance(function, GeneratorType):
			raise TypeError('Target must be GeneratorType')
		try:
			while not self._do_quit:
				self._new_messages.acquire()  # waits until at least 1 message is in the queue.
				with self._queue_access:
					raw_event = self._queue.popleft()  # pop oldest item
					msg = self.interface.new_event(raw_event)
					logger.debug('Messages waiting in queue: %d', len(self._queue))
				function.send(msg)
		except GeneratorExit:
			pass
		except KeyboardInterrupt:
			raise StopIteration



class MessageConstructorSuperclass(object):
	def new_event(self, raw_event):
		raise NotImplementedError("new_event() is not implemented")