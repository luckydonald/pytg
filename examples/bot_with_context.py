"""
Demonstrates how you could easily do complex conversations.
This conversation consists of the following:

You send
> /start

The bot welcomes you, and asks for your name


You send your name
> Luckydonald

The bot asks you for your age
> 4458

The bots replies with your name and age.

You are done, you now can continue from the beginning.

(after your `/start` until you are done, everyone else will only get a message, saying the bot is currently in use by another user)
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


@coroutine
def message_loop(sender):  # name "message_loop" and given parameters are defined in main()
    try:
        while True:  # loop for a session.
            msg = (yield)
            if should_skip_message(msg, sender):
                continue
            if msg.text.strip() != "/start":
                sender.msg(msg.sender.cmd, u"Please use the /start command.")
                continue  # go to the top of the while loop again.
            # end if

            user = msg.sender.cmd  # store his user cmd, we only want to chat with him now.
            sender.msg(user, u"Welcome. Please tell me your name.")

            msg = (yield)  # get the next message
            while should_skip_message(msg, sender, only_allow_user=user):
                # If msg is a unwanted event/message, get the next one.
                # See should_skip_message for more detail.
                msg = (yield)  # just get the next message.
            # end skip-while-unwanted loop

            name = msg.text
            sender.msg(user, u"Now {name}, how old are you?".format(name=name))

            msg = (yield)  # get the next message
            while should_skip_message(msg, sender, only_allow_user=user):
                # If msg is a unwanted event/message, get the next one.
                # See should_skip_message for more detail.
                msg = (yield)  # just get the next message.
            # end skip-while-unwanted loop

            age = msg.text

            sender.msg(
                msg.sender.cmd,
                u"Cool {name}, being {age} years old was the best time of my life!".format(name=name, age=age)
            )
            # done.
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass


def should_skip_message(msg, sender, only_allow_user=None):
    """
    Checks if the event is a message, is not from the bot itself, is in a user-to-user (user-to-bot) chat and has text.
    Also sets the online status to online.
    :keyword only_allow_user: (Optional) Ignore all messages which are not from this user (checks msg.sender.cmd)

    Basically the same code as in bot_ping.py, a little bit extended.
    """
    sender.status_online()  # so we will stay online.
    # (if we are offline it might not receive the messages instantly,
    #  but eventually we will get them)
    print(msg)
    if msg.event != "message":
        return True  # is not a message.
    if msg.own:  # the bot has send this message.
        return True  # we don't want to process this message.
    if msg.receiver.type != "user":
        return True
    if "text" not in msg or msg.text is None:  # we have media instead.
        return True  # and again, because we want to process only text message.
        # Everything in pytg will be unicode. If you use python 3 thats no problem,
        # just if you use python 2 you have to be carefull! (better switch to 3)
        # for convinience of py2 users there is a to_unicode(<string>) in pytg.encoding
        # for python 3 the using of it is not needed.
        # But again, use python 3, as you have a chat with umlaute and emojis.
        # This WILL brake your python 2 code at some point!
    if only_allow_user is not None and msg.sender.cmd != only_allow_user:
        sender.msg(msg.sender.cmd, u"I am currently in use by another user. Please try again later.")
        return True
    return False


# # program starts here # #
if __name__ == '__main__':
    main()  # executing main function.
    # Last command of file (so everything needed is already loaded above)
