# -*- coding: utf-8 -*-
"""
A simple example printing infos about yourself (i.e. your bot)
"""

from pytg.sender import Sender

__author__ = 'luckydonald'

s = Sender("127.0.0.1", 4458)
res = s.get_self()
print("Got: >%s<" % res)
username = res.username
print("my username is {user}".format(user=username))
