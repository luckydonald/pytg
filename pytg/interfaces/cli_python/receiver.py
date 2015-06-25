# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

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

	def start(self):
		tgl.on_msg_receive(self._get_message)
		tgl.on_binlog_replay_end(self._enable_listeneng)

	def stop(self):
		tgl.on_msg_receive()

	def __init__(self):
		super(Receiver, self).__init__()
		self._can_listen = False