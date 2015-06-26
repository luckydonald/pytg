# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

import pytg
from pytg import interfaces

def main():
	receiver = interfaces.automatic.receiver.Receiver(port=4458)  # get a Receiver Connector instance
	# If you use interfaces.automatic pytg will choose the best connection for you.
	# you can still provide all the parameters you'd give to the Receiver of one of the
	# interfaces (cli_python or interfaces.cli_socket). "Wrong" parameters will be ignored.

	receiver.start()	# start the Connector first, if you are concerned to
						# lose any messages (can happen with cli_socket only)

	receiver.register_event_loop(main_loop(receiver))
	# adds "main_loop" function (bellow) as listener. You can
	# directly supply arguments here (like receiver).


def main_loop(receiver):
	try:
		while True:
			msg = (yield)
			print('Full dump: {}'.format(msg))
			if isinstance(msg, pytg.types.Message):
				# so this is not an event (user joined etc) or such.
				print("Text: {}".format(msg.text))
		# end while
		print("loop ended.")
		receiver.stop()
	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")
	except GeneratorExit:
		# continues here, after exiting while loop in example_function()
		receiver.stop()
		logger.exception("after loop.")

logging.basicConfig(level=logging.DEBUG)




if __name__ != '__main__':  # not launched directly, probably cli.  This imports my debugger, and pytg from disk.
							# You should have pytg installed already via pip. So remove this line.
	import sys
	sys.path.append("/path/to/pycharm_debugger/pycharm-debug-py3k.egg")  # not needed.
	sys.path.append("/path/to/pytg")
	try:
		import pydevd
		pydevd.settrace('localhost', port=4457, stdoutToServer=True, stderrToServer=True, suspend=False)
	except ImportError:
		logger.warning("Failed to import debugger.")


main()