# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

import sys
sys.path.append("/path/to/pycharm_debugger/pycharm-debug-py3k.egg")
sys.path.append("/path/to/pytg")
try:
	import pydevd
	pydevd.settrace('localhost', port=4457, stdoutToServer=True, stderrToServer=True, suspend=True)
except ImportError:
	logger.warning("Failed to import debugger.")

import pytg
from pytg.utils import coroutine
from pytg.receiver import Receiver


@coroutine
def example_function(receiver):
	try:
		while True:
			msg = (yield)
			print('Full dump: {array}'.format(array=str( msg )))
	except KeyboardInterrupt:
		receiver.stop()
		print("Exiting")

logging.basicConfig(level=logging.DEBUG)
if pytg.has_tgl: # prefer tgl.
	from pytg.interfaces.cli_python.receiver import Receiver
	receiver = Receiver()
else:
	from pytg.interfaces.cli_socket.receiver import Receiver
	receiver = Receiver(port=4458) #get a Receiver Connector instance
receiver.start() #start the Connector.
print("ololll!")
receiver.for_each_event(example_function(receiver)) # add "example_function" function as listeners. You can supply arguments here (like receiver).
# continues here, after exiting while loop in example_function()
receiver.stop()
