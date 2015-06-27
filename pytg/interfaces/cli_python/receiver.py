# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import threading
import logging
logger = logging.getLogger(__name__)

import tgl
from .message_constructor import MessageConstructor
from ..access import PublicInterface
from ...utils import skip_yield


class Receiver(PublicInterface):
	def stop(self):
		super(Receiver, self).stop()

	def _enable_listeneng(self):
		"""
		stop ignoring messages.
		Used to not catch old messages.
		:return:
		"""
		self._can_listen = True

	def _get_message(self, obj):
		if not self._can_listen:
			return
		self._add_message(obj)
	def _thread_bump_(self):
		"""
		Used to get tgl's python time
		:return:
		"""
		pass

	def _routine_wrapper(self, function):
		"""
		prepare a wrapper function for self._routine where the needed parameters are already filled in.

		:param function: the generator function given to register_event_loop, which is needed to call self._routine(function)
		"""
		def _wrap():
			"""
			called by tgl's on_loop.
			"""
			self._routine(function)
		return _wrap

	def register_event_loop(self, function):
		"""
		Apply your function here. The function must contain a while loop,
		and receive the events from the yield statement.

		:param function: The function which contains the proccessing loop.
		:return: None
		"""
		skip_yield(function)
		tgl.set_on_loop(self._routine_wrapper(function))


	def _receiver(self):
		tgl.set_on_msg_receive(self._get_message)
		tgl.set_on_binlog_replay_end(self._enable_listeneng)

	#def stop(self):
	#	tgl.set_on_msg_receive()

	def __init__(self, *args, foobar=False, **kwargs):
		super(Receiver, self).__init__()
		self._can_listen = False
		self.message_constructor = MessageConstructor()
		self._block_generator_routine = False