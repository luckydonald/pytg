# -*- coding: utf-8 -*-
from pytg.sender import Sender

__author__ = 'luckydonald'


s = Sender("127.0.0.1", 4458)
res = s.get_self()
print("Got: >%s<" % res)
print("my username is {}".format(res.username))
