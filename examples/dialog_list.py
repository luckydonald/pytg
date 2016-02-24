# -*- coding: utf-8 -*-
__author__ = 'luckydonald'


def main():
    from pytg.sender import Sender
    x = Sender("127.0.0.1", 4458)
    res = x.dialog_list()
    print("Got: >%s<" % res)


if __name__ == '__main__':
    main()
