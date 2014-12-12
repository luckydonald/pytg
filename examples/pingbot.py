#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
An example to create a telegram bot which response to ping message in a
specified chat group with flood control. The bot will exit when receive quit
command from a specified user id.


		The msg array object:
		----------------------

		msg.peer: Peer.GROUP or Peer.USER
		msg.user: Peer object containing the user
		msg.group: Peer object containing the group chat or None, if not GROUP message.
		msg.reply: Peer object containing the group chat or the user chat object if not GROUP message.


		The Peer() object:
		-------------------

		msg.user.type = Peer.GROUP or Peer.USER
		cmd = "chat#123" or "user#456" (peer identifier + hashtag + id)   Safe way to address a message
		name = "Random Chat #1" or "I am a User."
		id = 123 (a number)
		namecmd = "Random_Chat_@1" or "I_am_a_User."    (username with '_' for spaces and '@' instead of '#')
														This is the deprecated way of addressing user/groups



	tl;dr
	--------

		To anwer to an message in the same chat as the received message, use the data of msg.reply .

		To get the sender peer string   use .cmd on an Peer object.  E.g. msg.reply.cmd
		To identify a user              use msg.user.id
		To get the user/chatroom name   use msg.user.name or msg.group.name


"""

from datetime import datetime, timedelta
import pytg
from pytg.utils import coroutine, broadcast
from pytg.tg import message


QUIT = False
ADMIN_USERID = 1234567
# Bot will respond to command the posted in this chat group
CHAT_GROUP = 'kangkung for dummies'
# I like that name, it is still from the forked original.


#The program starts way at the bottom. Look for the
# if __name__ == "__main___"           statement.

@coroutine
def command_parser(tg):
    global QUIT
    global ADMIN_USERID
    global CHAT_GROUP
    last_ping = None
    # To avoid ping flood attack, we'll respond to ping once every 10 sec
    mydelta = timedelta(seconds=10)
    try:
        while True:
            msg = (yield)
            """""""""""""""""""""""""""""""""""""""""""""
             ^- the msg array object. (see the doc at top)
            """""""""""""""""""""""""""""""""""""""""""""
            # Only process if the group name match
            if msg.group.name == CHAT_GROUP:
                cmd = msg.message.strip().split(' ')
                if len(cmd) == 1:
                    # ping command
                    if cmd[0].lower() == 'ping':
                        now = datetime.now()
                        # simple ping flood control
                        if not last_ping or (now - last_ping) >= mydelta:
                            last_ping = now
                            # Send pong respond to this chat group
                            tg.msg(msg.reply.cmd, 'pong')
                    # quit command
                    elif cmd[0].lower() == 'quit':
                        if msg.user.id == ADMIN_USERID: # Checking user id
                            tg.msg(msg.reply.cmd, 'By your command.') #reply to same chat (group or user)
                            tg.msg(msg.user.cmd, 'Good bye.') #reply to user directly
                            QUIT = True
    except GeneratorExit:
        pass

if __name__ == '__main__':
    import os

    # Your relative paths here.
    telegram = 'tg-for-pytg2/bin/telegram-cli'
    pubkey = 'tg-for-pytg2/server.pub'

    # transform to absolute paths
    telegram = os.path.abspath(telegram)
    pubkey = os.path.abspath(pubkey)

    print("Loading telegram from %s, with key %s." % (telegram, pubkey))

    # Instantiate Telegram class.  This tg thing is needed to do all this fancy things.
    tg = pytg.Telegram(telegram, pubkey)

    # Create processing pipeline
    pipeline = message(command_parser(tg)) # we can give parameters to our function command_parser().
                                           #  Like we do with tg.

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
    tg.safe_quit()

