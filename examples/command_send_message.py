# -*- coding: utf-8 -*-
"""
Simplest way to just send a message.
Without complicated message receiving stuff.
"""
from pytg.sender import Sender
__author__ = 'luckydonald'


def main():
    sender = Sender("127.0.0.1", 4458)
    # you need a CLI already running in json mode on port 4458.

    res = sender.msg("@username", "Hello!")
    print("Response: {response}".format(response=res))
# end def main

if __name__ == '__main__':
    main()