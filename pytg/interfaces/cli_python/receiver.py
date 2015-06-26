# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import threading
import logging
logger = logging.getLogger(__name__)

import tgl

from .message_constructor import MessageConstructor
from ..access import PublicInterface


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
		def _wrap():
			self._routine(function)
		return _wrap

	def for_each_event(self, function):
		#assert self._routine_func is None # there is not already a function registered.
		#self._routine_func = function
		tgl.set_on_loop(self._routine_wrapper(function))
		#self._main_tread = threading.Thread(name="Main Thread (pytg, via cli's tgl)", target=self._routine, args=(function,))
		#self._main_tread.daemon = False  # exit if script reaches end.
		#self._main_tread.start()

	def _receiver(self):
		tgl.set_on_msg_receive(self._get_message)
		tgl.set_on_binlog_replay_end(self._enable_listeneng)

	#def stop(self):
	#	tgl.set_on_msg_receive()

	def __init__(self):
		super(Receiver, self).__init__()
		self._can_listen = False
		self.message_constructor = MessageConstructor()
		self._block_generator_routine = False