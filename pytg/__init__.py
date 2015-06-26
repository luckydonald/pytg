# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)


VERSION = "0.5.2dev0" # dev version.

try:
	import tgl
	has_tgl = True
except ImportError:
	has_tgl = False
# end try

from .interfaces.access import PublicInterface
from . import types

