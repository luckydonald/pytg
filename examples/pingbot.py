#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An example to create a telegram bot which response to ping message in a
specified chat group with flood control. The bot will exit when receive quit
command from a specified user id.
"""

from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import (
    dialog_list, chat_info, message, user_status,
)

QUIT = False

@coroutine
def command_parser(chat_group, tg):
    global QUIT
    last_ping = None
    # To avoid ping flood attack, we'll respond to ping once every 10 sec
    mydelta = timedelta(seconds=10)
    try:
        while True:
            msg = (yield)
            # Only process if the group name match
            if msg['group'] == chat_group:
                cmd = msg['message'].strip().split(' ')
                if len(cmd) == 1:
                    # ping command
                    if cmd[0].lower() == 'ping':
                        now = datetime.now()
                        # simple ping flood control
                        if not last_ping or (now - last_ping) >= mydelta:
                            last_ping = now
                            # Send pong respond to this chat group
                            tg.msg(msg['cmdgroup'], 'pong')
                    # quit command
                    elif cmd[0].lower() == 'quit':
                        if msg['uid'] == '1234567': # Put your user id here
                            tg.msg(msg['cmdgroup'], 'By your command')
                            QUIT = True
    except GeneratorExit:
        pass

if __name__ == '__main__':
    # Instantiate Telegram class
    telegram = './telegram'
    pubkey = 'tg.pub'
    tg = pytg.Telegram(telegram, pubkey)

    # Create processing pipeline
    # Bot will respond to command the posted in this chat group
    grpname = 'kangkung for dummies'
    pipeline = message(command_parser(grpname, tg))

    # Register our processing pipeline
    tg.register_pipeline(pipeline)

    # Start telegram cli
    tg.start()
    while True:
        # Keep on polling so that messages will pass through our pipeline
        tg.poll()

        if QUIT:
            break

    # Quit gracefully
    tg.quit()
