# -*- coding: utf-8 -*-
import logging
import re

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)


mark_read = re.compile("^User (?P<user>[^\s]+) marked read (?P<outbox>\d+) outbox and (?P<inbox>\d+) inbox messages$",
                       re.UNICODE)




all = [
    (mark_read, "mark_read"),
]