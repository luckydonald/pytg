from pytg2.sender import NoResponse

__all__ = ["receiver", "sender"]

class Telegram(object):
	def __init__(self, host="127.0.0.1", port_receive=4458, port_send=1337, telegram = None, pubkey_file = None):
		from .sender import Sender
		from .receiver import Receiver
		if telegram and pubkey_file:
			self.startCLI(telegram=telegram, pubkey_file=pubkey_file, port_receive=port_receive, port_send=port_send)
			host = "127.0.0.1"
		self.sender = Sender(host=host,port=port_send)
		self.receiver = Receiver(host=host,port=port_receive)


	def startCLI(self, telegram=None, pubkey_file=None, port_receive=4458, port_send=1337):
		"""
		Start the telegram process.

		:return: (int) process id of telegram.
		"""
		if not telegram or not pubkey_file:
			raise ValueError("telegram and/or pubkey_file not defined.")
		self._tg = telegram
		self._pub = pubkey_file
		import subprocess
		import platform

		def preexec_function():
			def on_abort(signal, stackframe):
				print("SIGINT ignored!")
				return False
			# Ignore the SIGINT signal by setting the handler
			# to the standard signal handler SIG_IGN.
			# Does this even work ?!?
			import signal
			signal.signal(signal.SIGINT, on_abort)
		self._proc = subprocess.Popen([self._tg, '-R', '-s','127.0.0.1:' + str(port_receive), '-P', str(port_send), '-W',  '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn = preexec_function)
		return self._proc.pid
		#return pid
		raise NotImplementedError("I Have to figure out processes in Python first...")

	def stopCLI(self):
		try:
			self.sender.safe_quit()
		except NoResponse:
			pass
		self._proc.poll()
		if self._proc.returncode:
			return self._proc.returncode
		self._proc.terminate()
		self._proc.poll()
		if self._proc.returncode:
			return self._proc.returncode
		self._proc.kill()
		self._proc.poll()
		return self._proc.returncode