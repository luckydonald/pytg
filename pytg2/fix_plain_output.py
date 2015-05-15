# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging

logger = logging.getLogger(__name__)

import re

mark_read = re.compile("^User (?P<user>[^\s]+) marked read (?P<outbox>\d+) outbox and (?P<inbox>\d+) inbox messages$", re.UNICODE)




all = [
	(mark_read, "mark_read"),
	   ]