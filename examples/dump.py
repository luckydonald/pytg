#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An example to dump all parsed messages from telegram cli to stdout
"""

import sys
from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
)

@coroutine
def dump_msg():
    try:
        while True:
            msg = (yield)
            print(msg)
    except GeneratorExit:
        pass

if __name__ == '__main__':
    # Instantiate Telegram class
    telegram = './telegram'
    pubkey = 'tg.pub'
    tg = pytg.Telegram(telegram, pubkey)

    # Create processing pipeline
    # All messages will be process and finally pushed to dump_msg
    d = dump_msg()
    pipeline = broadcast([
        message(d),
        user_status(d),
        dialog_list(d),
        chat_info(d),
    ])

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    while True:
        # Keep on polling so that messages will pass through our pipeline
        tg.poll()

    # Quit gracefully
    tg.quit()
