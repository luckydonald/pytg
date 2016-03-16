"""
This will show how you could use `message_get` command and the `reply_id` information.

To activate the bot, reply to any message with the text "#top"
If the bot receives such reply, it will look up the original message.
If that is a reply too, it will continue further.
Eventually the bot will reply to the first message the replies are pointing on.
"""

from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine

__author__ = 'luckydonald'


def main():
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.

    # add "example_function" function as message listener. You can supply arguments here (like sender).
    receiver.message(message_loop(sender))  # now it will call the example_function and yield the new messages.

    # continues here, after exiting the while loop in example_function()

    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
    receiver.stop()

    # continues here, after exiting while loop in example_function()
    print("I am done!")

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.


# end def main

def get_message_replied_to(msg, sender):
    if 'reply_id' in msg:
        next_msg = sender.message_get(msg.reply_id)
        return get_message_replied_to(next_msg, sender)
    return msg


@coroutine
def message_loop(sender):  # name "message_loop" and given parameters are defined in main()
    try:
        while True:  # loop for messages
            # ==================== #
            # SAME CODE as bot_dump.py #
            # ==================== #
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
            # ======================== #
            # OUR NEW CODE STARTS HERE #
            # ======================== #
            if msg.text.strip() == "#top":
                source = get_message_replied_to(msg, sender)
                sender.reply(source.id, "This is the top one.")
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass


# # program starts here # #
if __name__ == '__main__':
    main()  # executing main function.
    # Last command of file (so everything needed is already loaded above)