# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import fcntl
import struct
from utils import start_pipeline

class TelegramError(Exception):
	pass

class Telegram(object):
	_proc, tgin = None, None
	_pipeline, _callables = None, []
	_buffer, _banner_found = '', False
	_ignore = ['> \n','>\n']
	ready = False
	def __init__(self, telegram, pubkey_file):
		self._tg = telegram
		self._pub = pubkey_file

	def register_pipeline(self, pipeline):
		self._pipeline = start_pipeline(pipeline)

	def register_callable(self, func, *args, **kwargs):
		self._callables.append([func, args, kwargs])

	def start(self):
		def preexec_function():
			import signal
			# Ignore the SIGINT signal by setting the handler
			# to the standard signal handler SIG_IGN.
			signal.signal(signal.SIGINT, signal.SIG_IGN)
		proc = subprocess.Popen([self._tg, '-R', '-N', '-W', '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn = preexec_function)
		self._proc, self.tgin = proc, proc.stdin
		fd = proc.stdout.fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

	def poll(self):
		if not self._proc or self._proc.poll():
			raise TelegramError('telegram not running')

		try:
			c = self._proc.stdout.read(1)
		except:
			c = ''
		self._buffer += c
		if not self._banner_found and c == '\n' and 'conditions' in self._buffer:
			self._banner_found = True
			self._buffer = ''
			self.ready = True
		if self._banner_found and c == '\n':
			if '{print_message}' in self._buffer:
				if '{end_print_message}' in self._buffer:
					self._pipeline.send(self._buffer)
					self._buffer = ''
			else:
				if self._buffer not in self._ignore:
					self._pipeline.send(self._buffer)
				self._buffer = ''

	def quit(self):
		self._proc.communicate('quit\n')
		if len(self._buffer) > 0:
			self._pipeline.send(self._buffer)
		self._pipeline.close()

	def safe_quit(self):
		self._proc.communicate('safe_quit\n')
		if len(self._buffer) > 0:
			self._pipeline.send(self._buffer)
		self._pipeline.close()

	def force_quit(self):
		try:
			self._pipeline.close()
		except:
			pass
		self._proc.terminate()


	def msg(self, peer, message):
		self.tgin.write(' '.join(['msg', peer, message]) + '\n')
		self.tgin.flush()

	def send_audio(self, peer, path):
		self.tgin.write(' '.join(['send_audio', peer, path]) + '\n')
		self.tgin.flush()

	def send_contact(self, peer, phone, first_name, last_name):
		self.tgin.write(' '.join(['send_contact', peer, phone, first_name, last_name]) + '\n')
		self.tgin.flush()

	def send_document(self, peer, path):
		self.tgin.write(' '.join(['send_document', peer, path]) + '\n')
		self.tgin.flush()

	def send_photo(self, peer, path):
		self.tgin.write(' '.join(['send_photo', peer, path]) + '\n')
		self.tgin.flush()

	def send_video(self, peer, path):
		self.tgin.write(' '.join(['send_video', peer, path]) + '\n')
		self.tgin.flush()

	def send_location(self, peer, latitude, longitude):
		self.tgin.write(' '.join(['send_location', peer, latitude, longitude]) + '\n')
		self.tgin.flush()

	def send_text(self, peer, path):
		self.tgin.write(' '.join(['send_text', peer, path]) + '\n')
		self.tgin.flush()

	def status_online(self):
		self.tgin.write('status_online\n')
		self.tgin.flush()

	def status_offline(self):
		self.tgin.write('status_offline\n')
		self.tgin.flush()


	def dialog_list(self):
		self.tgin.write('dialog_list\n')
		self.tgin.flush()

	def chat_info(self, chat):
		self.tgin.write(''.join(['chat_info ', chat, '\n']))
		self.tgin.flush()

	def chat_add_user(self, chat, user, msgs_to_forward="100"):
		"""
		Adds user to chat. Sends him last msgs_to_forward message from this chat. Default "100"
		"""
		self.tgin.write(' '.join(['chat_add_user', chat, user,msgs_to_forward]) + '\n')
		self.tgin.flush()

	def chat_del_user(self, chat, user):
		"""
		Deletes user from chat
		"""
		self.tgin.write(' '.join(['chat_del_user', chat, user]) + '\n')
		self.tgin.flush()


	def user_info(self, user):
		self.tgin.write(''.join(['user_info ', user, '\n']))
		self.tgin.flush()

	def mark_read(self, peer):
		self.tgin.write(''.join(['mark_read ', peer, '\n']))
		self.tgin.flush()

	def chat_with_peer(self, peer):
		self.tgin.write(''.join(['chat_with_peer ', peer, '\n']))
		self.tgin.flush()

	def contact_list(self):
		self.tgin.write('contact_list\n')
		self.tgin.flush()

	def del_contact(self, user):
		self.tgin.write(''.join(['del_contact ', user, '\n']))
		self.tgin.flush()

	def fwd(self, peer, msg_id):
		self.tgin.write(' '.join(['fwd', peer, msg_id,'\n']))
		self.tgin.flush()

	def fwd_media(self, peer, msg_id):
		self.tgin.write(' '.join(['fwd_media', peer, msg_id,'\n']))
		self.tgin.flush()

	def raw_input(self, raw):
		self.tgin.write(''.join([raw,'\n']))
		self.tgin.flush()


	def chat_set_photo(self, chat, path):
		"""
		Sets chat photo. Photo will be cropped to square
		"""
		self.tgin.write(' '.join(['chat_set_photo', chat, path]) + '\n')
		self.tgin.flush()

	def set_profile_photo(self, path):
		"""
		Sets profile photo. Photo will be cropped to square
		"""
		self.tgin.write(' '.join(['set_profile_photo', path]) + '\n')
		self.tgin.flush()

	def export_card(self):
		"""
		Prints card that can be imported by another user with import_card method
		"""
		self.tgin.write('export_card\n')
		self.tgin.flush()

	def import_card(self,card):
		"""
		Gets user by card and prints it name. You can then send messages to him as usual
		:param card: Is a String like 0301adca:42eb522a:2f02aca9:4562e9f1:586a195b
		"""
		self.tgin.write(' '.join(['import_card', card]) + '\n')
		self.tgin.flush()

	def main_session(self):
		"""
		Sends updates to this connection (or terminal). Useful only with listening socket
		"""
		self.tgin.write('main_session\n')
		self.tgin.flush()

	# load_photo <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_photo(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_photo', peer, msg_id,'\n']))
		self.tgin.flush()

	# load_video <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_video(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_video', peer, msg_id,'\n']))
		self.tgin.flush()


	# load_audio <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_audio(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_audio', peer, msg_id,'\n']))
		self.tgin.flush()

	# load_document <msg-id>  Downloads file to downloads dirs. Prints file name after download end
	def load_document(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_document', peer, msg_id,'\n']))
		self.tgin.flush()

	# load_video_thumb <msg-id>       Downloads file to downloads dirs. Prints file name after download end
	def load_video_thumb(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_video_thumb', peer, msg_id,'\n']))
		self.tgin.flush()

	# load_document_thumb <msg-id>    Downloads file to downloads dirs. Prints file name after download end
	def load_document_thumb(self, peer, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(' '.join(['load_document_thumb', peer, msg_id,'\n']))
		self.tgin.flush()



def whoami(self):
	if 'HOME' in os.environ:
		authfile = os.path.join(os.environ['HOME'], '.telegram', 'auth')
		if os.path.exists(authfile):
			with open(authfile, 'rb') as fh:
				fh.seek(-4, 2)
				myid = struct.unpack('<I', fh.read(4))[0]
			return str(myid)
		else:
			raise TelegramError("You have not registered telegram client")
	else:
		raise TelegramError("Undefined 'HOME' environment variable")
