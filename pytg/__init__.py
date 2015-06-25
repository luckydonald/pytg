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



if has_tgl:
	from .interfaces import cli_python as telegram_interface
else:
	from .interfaces import cli_socket as telegram_interface
# end if
