# coding=utf-8
from __future__ import unicode_literals
from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine

__author__ = 'luckydonald'

ADMIN_ID = 10717954  # you should probably change this.

def main():
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.

    # add "example_function" function as message listener. You can supply arguments here (like sender).
    receiver.message(example_function(sender))  # now it will call the example_function and yield the new messages.

    # continues here, after exiting the while loop in example_function()

    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
    receiver.stop()

    print("I am done!")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.


# this is the function which will process our incoming messages
@coroutine
def example_function(sender):  # name "example_function" and given parameters are defined in main()
    quit = False
    try:
        while not quit:  # loop for messages
            msg = (yield)  # it waits until the generator has a has message here.
            sender.status_online()  # so we will stay online.
            # (if we are offline it might not receive the messages instantly,
            #  but eventually we will get them)
            print(msg)
            if msg.event != "message":
                continue  # is not a message.
            if msg.own:  # the bot has send this message.
                continue  # we don't want to process this message.
            if msg.text is None:  # we have media instead.
                continue  # and again, because we want to process only text message.
            # Everything in pytg will be unicode. If you use python 3 thats no problem,
            # just if you use python 2 you have to be carefull! (better switch to 3)
            # for convinience of py2 users there is a to_unicode(<string>) in pytg.encoding
            # for python 3 the using of it is not needed.
            # But again, use python 3, as you have a chat with umlaute and emojis.
            # This WILL brake your python 2 code at some point!
            if msg.text == u"ping":
                sender.send_msg(msg.peer.cmd, u"Pöng!")  # unicode support :D
            elif msg.text == u"quit":  # you should probably check a user id
                if msg.sender.id == ADMIN_ID:
                    sender.send_msg(msg.sender.cmd, u"Bye!")
                    quit = True
                else:
                    reply = u"You are not my Admin.\nMy Admin has id {admin_id} but you have {user_id}".format(
                        admin_id=ADMIN_ID, user_id=msg.sender.id)
                    sender.send_msg(msg.sender.cmd, reply)
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass


# # program starts here ##
if __name__ == '__main__':
    main()  # executing main function.
    # Last command of file (so everything needed is already loaded above)