# -*- coding: utf-8 -*-
"""
Simpler example printing the list of chats you have.
"""
from pytg.sender import Sender
__author__ = 'luckydonald'


def main():
    x = Sender("127.0.0.1", 4458)
    result = x.dialog_list()
    print("Got: %s" % str(result))

if __name__ == '__main__':
    main()
