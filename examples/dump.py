#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An example to dump all parsed messages from telegram cli to stdout
"""

import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
    user_info, contact_list, service_message,
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
    telegram = 'tg-for-pytg2/bin/telegram-cli'
    pubkey = 'tg-for-pytg2/server.pub'

    # Instantiate Telegram class
    tg = pytg.Telegram(telegram, pubkey)

    # Get own id (integer represented as string datatype)
    myid = tg.whoami()

    # Variables that represents some states whether we're send some commands
    # to telegram
    has_send_contact_list = False
    has_send_user_info = False

    # Create processing pipeline
    # All messages will be process and finally pushed to dump_msg
    d = dump_msg()
    pipeline = broadcast([
        message(d),
        user_status(d),
        dialog_list(d),
        chat_info(d),
        user_info(d),
        contact_list(d),
        service_message(d),
    ])

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    try:
        while True:
            # Keep on polling so that messages will pass through our pipeline
            tg.poll()
            if tg.ready and not has_send_contact_list:
                tg.contact_list()
                has_send_contact_list = True
            if tg.ready and not has_send_user_info:
                tg.user_info('user#' + myid)
                has_send_user_info = True
    except KeyboardInterrupt:
        # Quit gracefully
        tg.quit()
