# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import socket # connect to telegram cli.
import time # wait for retry

SOCKET_SIZE = 1 << 25

class Telegram(object):
	QUIT = False

	def __init__(self):
		self.host = "127.0.0.1"
		self.port = 4458

	def init(self):
		while not self.QUIT:
			if s:
				s.close()
			del s;
			s = socket.socket()
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			failed = True
			while failed:
				try:
					s.bind(((self.host), self.port))
				except Exception as err:
					print(err)
					print("Port assignment Failed. Retring in 1 second.")
					time.sleep(1)
				else:
					failed = False
					print("Successful bound to port.")
			s.listen(1) # allow 1 connection.
			print("Listening!")
			conn, addr = s.accept()
			print("Got something %s , %s" %(str(conn), str(addr)))
			try:
				while not self.QUIT:
					result = conn.recv(SOCKET_SIZE)
					print("Got result: " + str(result))

					time.sleep(1)
			finally:
				s.close()

	def init(self):
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		try:
			self.s.connect(("localhost",self.port))
		except ConnectionRefusedError:
			print("Connection to gpio-server refused.\n Maybe not running?")
			return "Connection refused."
		except socket.error as err:
			print("Socket error:\n" + str(err))
			return "Socket error:\n" + str(err)
		else:
			self.connected = True
			return None

