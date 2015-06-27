# -*- coding: utf-8 -*-
"""
Import automatic to automatically get the cli_python connector
if tgl is available. (You started it in the thelegram-cli?)
"""

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from .. import has_tgl

if has_tgl:  # means we are run in tgl.
	from . import cli_python as automatic
	logger.debug("cli_python as automatic interface")
else:  # else socket.
	from . import cli_socket as automatic
automatic = automatic

__all__ = ["automatic", "cli_socket", "cli_python", "bot_api"]