#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
This will show how you could split logic processing into multiple_handlers
"""

from pytg import Telegram
from pytg.utils import coroutine

def main():

    tg = Telegram(
        telegram="/usr/bin/telegram-cli",
        pubkey_file="/etc/share/telegram-cli/server.pub"
	)

    # get a Receiver instance, to get messages.
    receiver = tg.receiver

    # get a Sender instance, to send messages, and other querys.
    sender = tg.sender

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.

    # add handlers to the receiver
    receiver.add_handler(text_handler(sender))
    receiver.add_handler(media_handler(sender))

    # start processing the handlers
    receiver.process_handlers()
    
    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
    receiver.stop()

    # continues here, after exiting while loop in example_function()
    print("I am done!")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.

# end def main

@coroutine
def text_handler(sender):
    try:
        while True:
            msg = (yield)
            print(msg)
            sender.status_online()
            
            if 'text' in msg and msg.text == "/hello":
                sender.reply(msg.id, 'detected text: ' + msg.text)
                
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, because _quit was set True
        pass
            
@coroutine
def media_handler(sender):
    try:
        while True:
            msg = (yield)
            sender.status_online()
            
            if 'media' in msg:
                sender.reply(msg.id, 'media detectado')
                
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, because _quit was set True
        pass
        
# # program starts here # #
if __name__ == '__main__':
    main()  # executing main function.
    # Last command of file (so everything needed is already loaded above)
