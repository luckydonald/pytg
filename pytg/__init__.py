# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import with_statement # This isn't required since Python 2.6
from __future__ import unicode_literals
import os
# import sys
import subprocess
import fcntl
import struct
from .utils import start_pipeline, escape, string_or_empty
from . import encoding
from .encoding import to_unicode as u
from .encoding import to_binary as b
from .encoding import to_native as n
from .errors import TelegramError

class Telegram(object):
	_debug_output_file = None
	_proc, tgin,_encoding = None, None, None
	_pipeline, _callables = None, []
	_buffer, _banner_found = n(''), False
	_buffer_char = b('')
	_ignore = ['> \n','>\n']
	ready = False

	def __init__(self, telegram, pubkey_file):
		self._tg = telegram
		self._pub = pubkey_file

	def set_debug_output(self, debug_output_file):
		self._debug_output_file = debug_output_file

	def register_pipeline(self, pipeline):
		self._pipeline = start_pipeline(pipeline)

	def register_callable(self, func, *args, **kwargs):
		self._callables.append([func, args, kwargs])

	def start(self):
		def preexec_function():
			def on_abort(signal, stackframe):
				print("SIGINT ignored!")
				return False
			# Ignore the SIGINT signal by setting the handler
			# to the standard signal handler SIG_IGN.
			# Does this even work ?!?
			import signal
			signal.signal(signal.SIGINT,on_abort)
		proc = subprocess.Popen([self._tg, '-R', '-N', '-W', '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn = preexec_function)
		self._proc, self.tgin = proc, proc.stdin
		fd = proc.stdout.fileno()
		fl = fcntl.fcntl(fd, fcntl.F_GETFL)
		fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

	def poll(self):
		if not self._proc or self._proc.poll():
			raise TelegramError('telegram not running')
		try:
			c = self._proc.stdout.read(1) # allways is a byte string.
		except TypeError:
			return # yeah. Nothing to do here,
		if c is None:
			return # yeah. Nothing to do here,

		try:
			if self._debug_output_file:
				with open(self._debug_output_file, "ab") as text_file:
					text_file.write(c)
		except Exception:
			raise # probably file io

		if len(self._buffer_char) > 0:  # already begun with an imcomplete character.
			self._buffer_char += c  # add this part to it.
			try:
				u_c = u(self._buffer_char)
			except UnicodeDecodeError:  # added character to char buffer, but is no complete character.
				return  # better luck next time.
			else:       # hey, it did work!
				self._buffer_char = b('')  # reset chraracter buffer
		else: # no incomplete character.
			try:
				u_c = u(c)  #try to parse current char
			except UnicodeDecodeError:  # is not a whole char.
				assert (len(self._buffer_char) == 0)
				self._buffer_char = c  # begin with adding incomplete character parts
				return  # better luck/part next time.
			else:  #is normal complete char
				pass  # wooho?
		self._buffer = "".join([self._buffer,u_c])

		if not self._banner_found and c == b'\n' and 'conditions' in self._buffer:
			self._banner_found = True
			self._buffer = ''
			self.ready = True
		if self._banner_found and c == b'\n':
			if '{print_message}' in self._buffer:
				if '{end_print_message}' in self._buffer:
					self._pipeline.send(n(self._buffer))
					self._buffer = ''
			else:
				if self._buffer not in self._ignore:
					self._pipeline.send(n(self._buffer))
				self._buffer = ''



	def quit(self):
		self._proc.communicate(b('quit\n'))
		if len(self._buffer) > 0:
			self._pipeline.send(self._buffer)
		self._pipeline.close()

	def safe_quit(self):
		self._proc.communicate(b('safe_quit\n'))
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
		"""
		Will send a message to the given peer.
		:param peer: the peer name, spaces ' ' needs to be replaced with '_', and '#' in names with '@'
		but you can also send to the id of chats, chat#123 for group chats and user#123 for user.
		:param message: message to send. Escaped characters, like '\n' or '\t' will result in an linefeed, tab etc.,
		 escape backslashes like '\\t' to send them as text.
		"""
		self.tgin.write(b(' '.join(['msg', peer, escape(message), '\n'])))
		self.tgin.flush()

	#broadcast <user>+ <text>	Sends text to several users at once
	def broadcast(self, message, user, *args):
		"""
		This sends the message to multible senders, most time.
		WARNING: misstyping one of the User might result in unexpected results,
		such as appending the provided user to the message and not sending to all receivers,
		braking of linefeeds, etc.
		DO NOT USE!!! use msg() instead!
		You could for example use a for loop.
		For the sake of completeness, it is still included, but will print an warnig every time used.

		:param message: The message.
		:param user: CORRECTLY spelled first user. (else it will become the message!)
		:param *args: more CORRECTLY spelled more users. (else it will become the message!)
		"""
		print("\nWARNING: It is not recommanded to use the broadcast method! If you misstype ANY given user will break "
		      "the Telegram commad, randomly append the given user names to the message text, and also not send to all "
		      "users!!!")
		self.tgin.write(b(' '.join(['broadcast', user, ' '.join(args), escape(message)]) + '\n'))
		self.tgin.flush()

	def send_audio(self, peer, path):
		self.tgin.write(b(' '.join(['send_audio', peer, path]) + '\n'))
		self.tgin.flush()

	def send_contact(self, peer, phone, first_name, last_name):
		self.tgin.write(b(' '.join(['send_contact', peer, phone, first_name, last_name]) + '\n'))
		self.tgin.flush()

	def send_document(self, peer, path):
		self.tgin.write(b(' '.join(['send_document', peer, path]) + '\n'))
		self.tgin.flush()

	def send_photo(self, peer, path):
		self.tgin.write(b(' '.join(['send_photo', peer, path]) + '\n'))
		self.tgin.flush()

	def send_video(self, peer, path):
		self.tgin.write(b(' '.join(['send_video', peer, path]) + '\n'))
		self.tgin.flush()

	def send_location(self, peer, latitude, longitude):
		self.tgin.write(b(' '.join(['send_location', peer, latitude, longitude]) + '\n'))
		self.tgin.flush()

	def send_text(self, peer, path):
		self.tgin.write(b(' '.join(['send_text', peer, path]) + '\n'))
		self.tgin.flush()

	def send_typing(self, peer):
		"""
		Sends "is typing..." event to peer.
		From my experience this status will just last for a few seconds, and has to be repeated, to last.
		:param peer: The peer where to 'type'.
		:return:
		"""
		self.tgin.write(b(' '.join(['send_typing', peer]) + '\n'))
		self.tgin.flush()

	def send_typing_abort(self, peer):
		"""
		Sends "is typing..." event to peer.
		Not sure what is difference from send_typing and send_typing_abort ...
		From my experience this does exactly the same as send_typing(), and the status will last for a few seconds,
		and has to be repeated, to last.
		:param peer: The peer where to 'type'.
		:return:
		"""
		self.tgin.write(b(' '.join(['send_typing', peer]) + '\n'))
		self.tgin.flush()


	def status_online(self):
		self.tgin.write(b('status_online\n'))
		self.tgin.flush()

	def status_offline(self):
		self.tgin.write(b('status_offline\n'))
		self.tgin.flush()

	def set_profile_name(self, first_name, last_name=None):
		"""
		Sets profile name.
		:param first_name: String.
		:param last_name: String, can be None
		"""
		last_name = "" if not last_name else last_name
		self.tgin.write(b(' '.join(['set_profile_name', escape(first_name), escape(last_name),'\n'])))
		self.tgin.flush()

	def set_username(self, username):
		"""
		Sets a username.
		Also seen as @username
		Can be searched globaly from all Telegram users,
		and can be accessed with http://telegram.me/username
		:param first_name: String.
		:param last_name: String, can be None
		"""
		self.tgin.write(b(' '.join(['set_username', escape(username),'\n'])))
		self.tgin.flush()

	def set_profile_photo(self, path):
		"""
		Sets profile photo. Photo will be cropped to square
		:param path: File path to the image.
		"""
		self.tgin.write(b(' '.join(['set_profile_photo', path]) + '\n'))
		self.tgin.flush()

	def dialog_list(self):
		self.tgin.write(b('dialog_list\n'))
		self.tgin.flush()

	def chat_info(self, chat):
		self.tgin.write(b(''.join(['chat_info ', chat, '\n'])))
		self.tgin.flush()

	# create_group_chat <user> <chat topic> - creates a groupchat with user, use chat_add_user to add more users
	# changed to
	# create_group_chat <name> <user>+	Creates group chat with users
	def create_group_chat(self,chat_topic,user,*args):
		"""
		creates a groupchat with user, use chat_add_user to add more users
		create_group_chat("testgroup","user1","user2","user3")
		:param chat_topic: name of the chat.  You should not include newline '\n' because
		the bot can't read that as the linebreaks brakes the parsed line in to 2 lines which will be parsed sepreatly.
		:param user: first user to add, you can add more, just pass more strings. For syntax see msg()
		:param args: arguments with the more users parameters.
		"""
		# TODO: Make sure no newline is in chat_topic.
		self.tgin.write(b(' '.join(['create_group_chat', escape(chat_topic), user, ' '.join(args)]) + '\n'))
		self.tgin.flush()

	def chat_add_user(self, chat, user, msgs_to_forward="100"):
		"""
		Adds user to chat. Sends him last msgs_to_forward message from this chat. Default "100"
		"""
		self.tgin.write(b(' '.join(['chat_add_user', chat, user,msgs_to_forward]) + '\n'))
		self.tgin.flush()

	def chat_del_user(self, chat, user):
		"""
		Deletes user from chat
		"""
		self.tgin.write(b(' '.join(['chat_del_user', chat, user]) + '\n'))
		self.tgin.flush()

	def chat_set_photo(self, chat, path):
		"""
		Sets chat photo. Photo will be cropped to square
		"""
		self.tgin.write(b(' '.join(['chat_set_photo', chat, path]) + '\n'))
		self.tgin.flush()

	def chat_set_name(self, chat, new_name):
		"""
		Alias for rename_chat because the default names are confusing.
		"""
		self.rename_chat(chat, new_name)

	# rename_chat <chat> <new name>	Renames chat
	def rename_chat(self, chat, new_name):
		"""
		Renames chat
		:param chat:  the chat
		:param new_name: new name, please do not include linebreaks, it will break the parsing of messages!
		(and also most clients display)
		"""
		# TODO: Make sure no newline is in chat_topic.
		self.tgin.write(b(' '.join(['rename_chat', chat, escape(new_name)]) + '\n'))
		self.tgin.flush()

	def user_info(self, user):
		self.tgin.write(b(''.join(['user_info ', user, '\n'])))
		self.tgin.flush()

	def mark_read(self, peer):
		self.tgin.write(b(''.join(['mark_read ', peer, '\n'])))
		self.tgin.flush()

	def chat_with_peer(self, peer):
		self.tgin.write(b(''.join(['chat_with_peer ', peer, '\n'])))
		self.tgin.flush()

	def contact_list(self):
		self.tgin.write(b('contact_list\n'))
		self.tgin.flush()

	def del_contact(self, user):
		self.tgin.write(b(''.join(['del_contact ', user, '\n'])))
		self.tgin.flush()

	def fwd(self, peer, msg_id):
		self.tgin.write(b(' '.join(['fwd', peer, msg_id,'\n'])))
		self.tgin.flush()

	def fwd_media(self, peer, msg_id):
		self.tgin.write(b(' '.join(['fwd_media', peer, msg_id,'\n'])))
		self.tgin.flush()

	def raw_input(self, raw):
		print(b(''.join([raw,'\n'])))
		self.tgin.write(b(''.join([raw,'\n'])))
		self.tgin.flush()

	def export_card(self):
		"""
		Prints card that can be imported by another user with import_card method
		"""
		self.tgin.write(b('export_card\n'))
		self.tgin.flush()

	def import_card(self,card):
		"""
		Gets user by card and prints it name. You can then send messages to him as usual
		:param card: Is a String like 0301adca:42eb522a:2f02aca9:4562e9f1:586a195b
		"""
		self.tgin.write(b(' '.join(['import_card', card]) + '\n'))
		self.tgin.flush()

	def main_session(self):
		"""
		Sends updates to this connection (or terminal). Useful only with listening socket.
		(Not sure what that does anyway?)
		"""
		self.tgin.write(b('main_session\n'))
		self.tgin.flush()

	# load_photo <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_photo(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_photo', msg_id,'\n'])))
		self.tgin.flush()

	# load_video <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_video(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_video', msg_id,'\n'])))
		self.tgin.flush()


	# load_audio <msg-id>     Downloads file to downloads dirs. Prints file name after download end
	def load_audio(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_audio', msg_id,'\n'])))
		self.tgin.flush()

	# load_document <msg-id>  Downloads file to downloads dirs. Prints file name after download end
	def load_document(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_document', msg_id,'\n'])))
		self.tgin.flush()

	# load_video_thumb <msg-id>       Downloads file to downloads dirs. Prints file name after download end
	def load_video_thumb(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_video_thumb', msg_id,'\n'])))
		self.tgin.flush()

	# load_document_thumb <msg-id>    Downloads file to downloads dirs. Prints file name after download end
	def load_document_thumb(self, msg_id):
		"""
		Downloads file to downloads dirs.
		"""
		self.tgin.write(b(' '.join(['load_document_thumb', msg_id,'\n'])))
		self.tgin.flush()

	#search [peer] [limit] [from] [to] [offset] pattern	Search for pattern in messages from date from to date to (unixtime) in messages with peer (if peer not present, in all messages)
	def search(self,pattern, peer=None, limit=None, from_unixtime=None, to_unixtime=None, offset=None):
		"""
		search for it.

		Note: Result from Telegram will be parsed and processed like normal incoming messages!

		:param pattern:
		:param peer:
		:param limit:
		:param from_unixtime:
		:param to_unixtime:
		:param offset:
		:return:
		"""
		self.tgin.write(b(' '.join(['search', string_or_empty(peer), string_or_empty(limit), string_or_empty(from_unixtime), string_or_empty(to_unixtime), string_or_empty(offset), escape(pattern), '\n'])))
		self.tgin.flush()
		string_or_empty()
		pass


	@staticmethod
	def whoami():
		if 'HOME' in os.environ:
			authfile = os.path.join(os.environ['HOME'], '.telegram-cli', 'auth')
			if os.path.exists(authfile):
				with open(authfile, 'rb') as fh:
					fh.seek(-4, 2)
					myid = struct.unpack('<I', fh.read(4))[0]
				return str(myid)
			else:
				raise TelegramError("You have not registered telegram client")
		else:
			raise TelegramError("Undefined 'HOME' environment variable")
