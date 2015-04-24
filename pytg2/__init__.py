from pytg2.sender import NoResponse
from pytg2.result_parser import IllegalResponseException
import atexit
__all__ = ["receiver", "sender"]

class Telegram(object):
	def __init__(self, host="127.0.0.1", port_receive=4458, port_send=1337, telegram = None, pubkey_file = None):
		from .sender import Sender
		from .receiver import Receiver
		if telegram and pubkey_file:
			if host not in ["127.0.0.1", "localhost","",None]:
				raise ValueError("Can only start the cli at localhost. You may not provide a different host.")
			host = "127.0.0.1"
			self.startCLI(telegram=telegram, pubkey_file=pubkey_file, port_receive=port_receive, port_send=port_send)
		self.sender = Sender(host=host,port=port_send)
		self.receiver = Receiver(host=host,port=port_receive)


	def startCLI(self, telegram=None, pubkey_file=None, port_receive=4458, port_send=1337):
		"""
		Start the telegram process.

		:return: (int) process id of telegram.
		"""
		print("Starting CLI.")
		if not telegram or not pubkey_file:
			raise ValueError("telegram and/or pubkey_file not defined.")
		self._tg = telegram
		self._pub = pubkey_file
		import subprocess
		def preexec_function():
			import os
			os.setpgrp()
		atexit.register(self.stopCLI)
		self._proc = subprocess.Popen([self._tg, '-R', '-s','127.0.0.1:' + str(port_receive), '-P', str(port_send), '-W',  '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn = preexec_function)
		return self._proc.pid
		#return pid
		#raise NotImplementedError("I Have to figure out processes in Python first...")

	def stopCLI(self):
		print("Stopping CLI.")
		try:
			self.sender.safe_quit()
		except (NoResponse, IllegalResponseException, AssertionError):
			pass
		self._proc.poll()
		if self._proc.returncode:
			return self._proc.returncode
		try:
			self._proc.terminate()
		except ProcessLookupError:
			pass
		self._proc.poll()
		if self._proc.returncode:
			return self._proc.returncode
		try:
			self._proc.kill()
		except ProcessLookupError:
			pass
		self._proc.poll()
		return self._proc.returncode