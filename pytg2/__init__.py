__all__ = ["receiver", "sender"]

class Telegram(object):
	def __init__(self, host="127.0.0.1", port_receive=4458, port_send=1337):
		from sender import Sender
		from receiver import Receiver

		self.sender = Sender(host=host,port=port_send)
		self.receiver = Receiver(host=host,port=port_receive)

	def startCLI(self, path):
		import subprocess

		return pid
