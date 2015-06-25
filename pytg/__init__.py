# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)


__all__ = ["receiver", "sender", "Telegram"]
VERSION = "0.5.1dev0" # dev version.

try:
	import tgl
	has_tgl = True
except ImportError:
	has_tgl = False
# end try

from .interfaces.access import PublicInterface

def new_interface(use_tgl=True, use_socket=False):
	has_interface = False
	if use_tgl:
		if has_tgl:
			from .interfaces.cli_python import receiver as receiver
			has_interface = True
		else:
			logger.warn("tgl package not found.")
	if not has_interface and use_socket:
		from .interfaces.cli_socket import receiver as receiver
		has_interface = True
	if not has_interface:
		raise ValueError("No interface selected")
	def add_receiver(*args):
		return PublicInterface(receiver.Receiver(*args))
	return add_receiver
# end if
