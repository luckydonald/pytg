__author__ = 'luckydonald'
from pytg2.receiver import Receiver # get messages
from pytg2.sender import Sender # send messages, and other querys.
from pytg2.utils import coroutine
from pytg2.encoding import to_unicode #also avialable:  to_binary, to_native



# see programm starts bellow, this is the function which will process our incoming messages
@coroutine
def example_function(sender):
	QUIT = False
	ADMIN_ID = 123456
	try:
		while not QUIT: # loop for messages
			msg = (yield) # it waits until it has a message here.

			if msg['out'] == True: # the bot has send this message.
				continue # we dont want to process this message.

			# Everything in ptg2 will be unicode. If you use python 3 thats no problem,
			# just if you use python 2 you have to be carefull! (better switch to 3)
			# for convinience of py2 users there is a to_unicode in pytg2.encoding
			# for python 3 the using of it is not needed.
			# But again, use python 3, as you have a chat with umlaute and emojis.
			# This WILL brake your python 2 code at some point!
			if msg['text'] == u"ping":
				sender.send_msg(msg['from']['print_name'], u"Pong!")

			elif msg['text'] == u"quit":  # you should probably check a user id
				if msg['from']['id'] == ADMIN_ID:
					sender.send_msg(msg['from']['print_name'], u"Bye!")
					QUIT = True
				else:
					reply = u"You are not my Admin.\nMy Admin has id {admin_id} but you have {user_id}".format(admin_id=ADMIN_ID, user_id=msg['from']['id'])
					sender.send_msg(msg['from']['print_name'], reply)
	except KeyboardInterrupt:
		print("Exiting")



## program start here ##
if __name__ == '__main__':
	# get a Receiver instance, to get messages.
	receiver = Receiver(host="localhost", port=4458)

	# get a Sender instance, to send messages, and other querys.
	sender = Sender(host="localhost" ,port=1337)

	#start the Receiver, so we can get messages!
	receiver.start()
	# note that the Sender has no need for a start function.

	# add "example_function" function as listeners. You can supply arguments here (like sender).
	receiver.message(example_function(sender))
	# now it will call the example_function and yield the new messages.

	# continues here, after exiting while loop in example_function()
	receiver.stop()

	# the sender will disconnect after each send, so there is not stop needed.

	# if you want to shutdown the telegram cli:
	# sender.safe_quit() # this shuts down the telegram cli.
