# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import threading
import socket # connect to telegram cli.

import pytgbot

from .message_constructor import MessageConstructor
from ..access import PublicInterface

import logging
logger = logging.getLogger(__name__)


class Receiver(PublicInterface):
	"""
	Start telegram client somewhere.
	$ ./bin/telegram-cli -P 4458 -W --json
	"""

	def __init__(self, api_key=None, *args, **kwargs):
		"""
		:keyword append_json: if the dict should contain the original json.
		:type    append_json: bool
		"""
		super(Receiver, self).__init__(*args,**kwargs)
		self.last_update = 0
		self.message_constructor = MessageConstructor()
		self.api_key = api_key
		self.connection = pytgbot.Bot(api_key)


	def start(self):
		"""
		Starts the receiver.
		When started, messages will be queued.
		:return:
		"""
		self._receiver_thread = threading.Thread(name="Receiver (pytg, via bot_api)", target=self._receiver, args=())
		self._receiver_thread.daemon = True  # exit if script reaches end.
		self._receiver_thread.start()


	def stop(self):
		"""
		Shuts down the receivers server.
		No more messages will be received.
		You should not try to start() it again afterwards.
		"""
		self._do_quit = True


	def _receiver(self):
		while not self._do_quit: # retry connection
			updates = self.connection.get_updates(offset=(self.last_update+1))
			if updates["ok"] == False:
				logger.warn("Skipping bad update(s): {}".format(updates))
				continue
			for update in updates["result"]:
				self.last_update = update["update_id"]
				self._add_message(update)
		# end while not ._do_quit: retry connection
	# end def _receiver(...)
# end class

