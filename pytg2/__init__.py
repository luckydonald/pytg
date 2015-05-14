import atexit
__all__ = ["receiver", "sender", "Telegram"]

import logging
logger = logging.getLogger(__name__)
from .exceptions import NoResponse, IllegalResponseException
#from .encoding import to_unicode as u


class Telegram(object):
	"""
	To have the sender and the receiver in one handsome object.
	Also is able to start the CLI, and stop it respectivly.
	"""
	def __init__(self, host="127.0.0.1", port=4458, telegram = None, pubkey_file = None, custom_cli_args = None):
		from .sender import Sender
		from .receiver import Receiver
		self._proc = None
		if telegram and pubkey_file:
			if host not in ["127.0.0.1", "localhost","",None]:
				raise ValueError("Can only start the cli at localhost. You may not provide a different host.")
			host = "127.0.0.1"
			self.startCLI(telegram=telegram, pubkey_file=pubkey_file, custom_cli_args=custom_cli_args, port=port)
		elif telegram is not None or pubkey_file is not None or custom_cli_args is not None:
			logger.warn("cli related parameter given, but not cli and pubkey path not present.")
		self.sender = Sender(host=host,port=port)
		self.receiver = Receiver(host=host,port=port)
		#NOTE: with the following while, if the cli has a message at boot, it will NOT ANSWER anything
		#      until that message got transmitted succsessfully. So it would block the foobar=Telegram(tg,key) call.

		#while self._proc is not None:
		#	result = self.sender.raw(u("help"))
		#	if result and u("Prints this help") in result:
		#		logger.info("CLI available.")
		#		break
		#	else:
		#		print("CLI does not response. (Debug: {})".format(result))



	def startCLI(self, telegram=None, pubkey_file=None, custom_cli_args=None, port=4458):
		"""
		Start the telegram process.

		:type telegram: builtins.str
		:type pubkey_file: builtins.str
		:type custom_cli_args: list | tuple
		:return: (int) process id of telegram.
		:rtype int:
		"""
		if not telegram or not pubkey_file:
			raise ValueError("telegram and/or pubkey_file not defined.")
		self._tg = telegram
		self._pub = pubkey_file
		import subprocess
		def preexec_function():
			import os
			os.setpgrp()
		atexit.register(self.stopCLI)
		args = [self._tg, '-R', '-W', '-P', str(port),  '-k', self._pub, '--json']
		if custom_cli_args is not None:
			if not isinstance(custom_cli_args, (list, tuple)):
				raise TypeError("custom_cli_args should be a list or a tuple.")
			args.extend(custom_cli_args)
		logger.info("Starting Telegram Executable: \"{cmd}\"".format(cmd=" ".join(args)))
		self._proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn = preexec_function)
		if self._check_stopped():
			raise AssertionError("CLI did stop, should be running...")
		#return pid
		#raise NotImplementedError("I Have to figure out processes in Python first...")

	def stopCLI(self):
		"""
		Stop the telegram process.

		:return: (int) returncode of the cli process.
		:rtype int:
		"""
		logger.info("Asking to CLI to stop.")
		if self._proc is not None:
			if self.sender._do_quit:
				logger.warn("Sender already stopped. Unable to issue safe_quit or quit to exit the cli nicely.")
			else:
				try:
					self.sender.safe_quit()
				except (NoResponse, IllegalResponseException, AssertionError):
					logger.debug("safe_quit Exception", exc_info=True)
				if self._check_stopped(): return self._proc.returncode
				logger.debug("safe_quit did not terminate.")

				try:
					self.sender.quit()
				except (NoResponse, IllegalResponseException, AssertionError):
					logger.debug("quit Exception", exc_info=True)
				if self._check_stopped(): return self._proc.returncode
				logger.debug("quit did not terminate.")
				self.sender.stop() # quit and safe quit are done, we don't need the sender any longer.
			#end if-else: self.sender._do_quit
			try:
				self._proc.terminate()
			except Exception as e: #todo: ProcessLookupError does not exist before python 3
				logger.debug("terminate Exception", exc_info=True)
			if self._check_stopped(): return self._proc.returncode
			logger.debug("terminate did not terminate.")

			try:
				self._proc.kill()
			except Exception as e: #todo:  ProcessLookupError does not exist before python 3
				logger.debug("kill Exception", exc_info=True)
			if self._check_stopped(): return self._proc.returncode
			logger.debug("kill did not terminate.")
			logger.warn("CLI kinda didn't die... Will wait (block) for termination.")

			self._proc.wait()
			self._check_stopped()
			return self._proc.returncode
		else:
			logger.warn("No CLI running.")
			raise AssertionError("No CLI running.")

	def _check_stopped(self):
		self._proc.poll()
		if self._proc.returncode is not None:
			logger.info("CLI did stop ({return_code}).".format(return_code=self._proc.returncode))
			if hasattr(self, "sender") and self.sender is not None:
				self.sender.stop()
			return True