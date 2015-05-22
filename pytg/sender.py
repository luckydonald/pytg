# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from . import result_parser as res
from . import argument_types as args
from .encoding import to_native as n
from .encoding import to_unicode as u
from .encoding import to_binary as b
from .encoding import text_type, binary_type
from .exceptions import UnknownFunction, ConnectionError, NoResponse, IllegalResponseException
from .fix_msg_array import fix_message
from .this_py_version import set_docstring

import json
import atexit
import socket # connect to telegram cli.
import inspect
import threading
from time import sleep
from DictObject import DictObject
from errno import ECONNREFUSED, EINTR
from socket import error as socket_error

import logging
logger = logging.getLogger(__name__)

SOCKET_SIZE = 1 << 25

FUNC_CMD  = 0
FUNC_ARGS = 1
FUNC_RES  = 2
FUNC_TIME = 3
__all__ = ["Sender"]
functions = {
	# function to call      # actual telegram command  # required arguments  # expected return type (parser)  # timeout (None = global default)

	# messages
	# send messages
	"send_text": 			("msg", 				[args.Peer("peer"), args.UnicodeString("test")],				res.success_fail, None),  # Sends text message to peer
	"send_audio": 			("send_audio", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0),
	"send_typing": 			("send_typing", 		[args.Peer("peer")],							res.success_fail, None),
	"send_typing_abort": 	("send_typing_abort", 	[args.Peer("peer")],													res.success_fail, None),
	"send_photo": 			("send_photo", 			[args.Peer("peer"), args.File("file"), args.UnicodeString("caption", optional=True)],											res.success_fail, 60.0),
	"send_video": 			("send_video", 			[args.Peer("peer"), args.File("file"), args.UnicodeString("caption", optional=True)],											res.success_fail, 60.0),
	"send_document": 		("send_document", 		[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0),
	"send_file": 			("send_file", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0),
	"send_location": 		("send_location", 		[args.Peer("peer"), args.Double("latitude"), args.Double("longitude")],							res.success_fail, None),
	"send_contact": 		("send_contact", 		[args.Peer("peer"), args.UnicodeString("phone"), args.UnicodeString("first_name"), args.UnicodeString("last_name")], res.something, 	60.0), #ret: formated message
	"send_text_from_file": 			("send_text", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0),
	"fwd": 					("fwd",		 				[args.Peer("peer"), args.MsgId("msg_id")],										res.success_fail, None),  # Forwards message to peer. Forward to secret chats is forbidden
	"fwd_media": 			("fwd_media", 			[args.Peer("peer"), args.MsgId("msg_id")],										res.success_fail, None),  # Forwards message media to peer. Forward to secret chats is forbidden. Result slightly differs from fwd
	"reply_text":			("reply", [args.MsgId("msg_id"), args.UnicodeString("text")], res.success_fail, None),  # Sends text reply to message
	"reply_audio":			("reply_audio", [args.MsgId("msg_id"),args.File("file")], res.success_fail, None),  # Sends audio to peer
	"reply_contact":		("reply_contact", [args.MsgId("msg_id"), args.UnicodeString("phone"), args.UnicodeString("first_name"), args.UnicodeString("last_name")], res.success_fail, None),  # Sends contact (not necessary telegram user)
	"reply_document":		("reply_document", [args.MsgId("msg_id"), args.File("file")], res.success_fail, None),  # Sends document to peer
	"reply_file":			("reply_file", [args.MsgId("msg_id"), args.File("file")], res.success_fail, None),  # Sends document to peer
	"reply_location":		("reply_location", [args.MsgId("msg_id"), args.Double("latitude"), args.Double("longitude")], res.success_fail, None),  # Sends geo location
	"reply_photo":			("reply_photo", [args.MsgId("msg_id"), args.File("file"), args.UnicodeString("caption", optional=True)], res.success_fail, None),  # Sends photo to peer
	"reply_video":			("reply_video", [args.MsgId("msg_id"), args.File("file"), args.UnicodeString("caption", optional=True)], res.success_fail, None),  # Sends video to peer
	"broadcast_text": 		("broadcast", [args.User("user", multible=True), args.UnicodeString("text")], res.success_fail, None),  # Sends text to several users at once

	# message related
	"message_delete": 		("delete_msg", 			[args.MsgId("msg_id")],													res.success_fail, None),  # Deletes message
	"message_get":			("get_message", [args.NonNegativeNumber("msg_id")], res.something, None),  # Get message by id
	"messages_search": 		("search", 				[
														args.Peer("peer", optional=True),
														args.NonNegativeNumber("limit", optional=True),
														args.NonNegativeNumber("from", optional=True),
														args.NonNegativeNumber("to", optional=True),
														args.NonNegativeNumber("offset", optional=True),
														args.UnicodeString("pattern")
													],							res.something, None),

	# load media
	"load_audio": 			("load_audio", 			[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_chat_photo":		("load_chat_photo", [args.Chat("chat")], res.success_fail, None),  # Downloads file to downloads dirs. Prints file name after download end
	"load_file":  			("load_file", 			[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_file_thumb":  	("load_file_thumb", 	[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_document": 		("load_document", 		[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_document_thumb":  ("load_document_thumb", [args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_photo":  			("load_photo", 			[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_video":  			("load_video", 			[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end
	"load_video_thumb":  	("load_video_thumb", 	[args.MsgId("msg_id")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end

	# peer
	"mark_read": 			("mark_read", 			[args.Peer("peer")],													res.success_fail, None),  # Marks messages with peer as read
	"history": 				("history", 			[args.Peer("user"), args.PositiveNumber("limit", optional=True), args.NonNegativeNumber("offset", optional=True)],							res.something, None),  # Prints messages with this peer (most recent message lower). Also marks messages as read


	# user
	"user_info": 			("user_info", 			[args.User("user")],													res.something, None),
	"load_user_photo":  	("load_user_photo", 	[args.User("user")],													res.something, 	60.0),  # Downloads file to downloads dirs. Prints file name after download end

	#contacts
	"contact_add": 			("add_contact", 		[args.UnicodeString("phone"), args.UnicodeString("first_name"), args.UnicodeString("last_name")], res.something, None),  # Tries to add user to contact list
	"contact_add_by_card":	("import_card", 		[args.UnicodeString("card")], res.success_fail, None),  # Gets user by card and prints it name. You can then send messages to him as usual #todo: add args type
	"contact_rename": 		("rename_contact", 		[args.User("user"), args.UnicodeString("first_name"), args.UnicodeString("last_name")],			res.something, None),  # Renames contact #returns the new name
	"contact_delete": 		("del_contact", 		[args.User("user")],													res.success_fail, None),  # Deletes contact from contact list
	"contacts_list": 		("contact_list", [], res.success_fail, None),  # Prints contact list
	"contacts_search": 		("contact_search", [args.UnicodeString("user_name"), args.NonNegativeNumber("limit", optional=True)], res.success_fail, None),  # Searches contacts by username

	# group chats
	"chat_info": ("chat_info", [args.Chat("chat")],													res.something, None),  # Prints info about chat (id, members, admin, etc.)
	"chat_set_photo": 		("chat_set_photo", 		[args.Chat("chat"), args.File("file")],								res.success_fail, None),  # Sets chat photo. Photo will be cropped to square
	"chat_add_user": 		("chat_add_user", 		[args.Chat("chat"), args.User("user"), args.NonNegativeNumber("msgs_to_forward", optional=True)],	res.something, 	60.0),  # Adds user to chat. Sends him last msgs-to-forward message from this chat. Default 100
	"chat_del_user": 		("chat_del_user", 		[args.Chat("chat"), args.User("user")],											res.success_fail, None),  # Deletes user from chat
	"chat_rename": 			("rename_chat", 		[args.Chat("chat"), args.UnicodeString("new_name")],			res.success_fail, None), # Renames chat
	"create_group_chat": 	("create_group_chat", 	[args.UnicodeString("name"), args.User("user", multible=True)],								res.success_fail, None),  # Creates group chat with users
	"import_chat_link": 	("import_chat_link", [args.UnicodeString("hash")], res.success_fail, None),  # Joins to chat by link
	"export_chat_link": 	("export_chat_link", [args.Chat("chat")], res.success_fail, None),  # Prints chat link that can be used to join to chat

	# secret chats
	"create_secret_chat": 	("create_secret_chat", 	[args.User("user")], res.success_fail, None),  # Starts creation of secret chat
	"accept_secret_chat": 	("accept_secret_chat", 	[args.SecretChat("secret_chat")],												res.success_fail, None),
	"set_ttl": 				("set_ttl", [args.NonNegativeNumber("secret_chat")], res.success_fail, None),  # Sets secret chat ttl. Client itself ignores ttl
	"visualize_key": 		("visualize_key", [args.SecretChat("secret_chat")], res.success_fail, None),  # Prints visualization of encryption key (first 16 bytes sha1 of it in fact}

	# own profile
	"set_profile_name": 	("set_profile_name", 	[args.UnicodeString("first_name"), args.UnicodeString("last_name")],	res.something, 	60.0),  # Sets profile name.
	"set_username": 		("set_username", 		[args.UnicodeString("name")], res.success_fail, None),  # Sets username.
	"set_profile_photo": 	("set_profile_photo", 	[args.File("file")],													res.something, 	60.0),  # Sets profile photo. Photo will be cropped to square
	"status_online": 		("status_online", 		[],																res.success_fail, None),  # Sets status as online
	"status_offline": 		("status_offline", 		[],																res.success_fail, None),  # Sets status as offline
	"export_card": 			("export_card", [], res.success_fail, None),  # Prints card that can be imported by another user with import_card method

	# system
	"quit": 				("quit", 				[],																res.response_fails, None),  # Quits immediately
	"safe_quit": 			("safe_quit",	 		[],																res.response_fails, None), # Waits for all queries to end, then quits
	"main_session": 		("main_session", [], res.success_fail, None),  # Sends updates to this connection (or terminal). Useful only with listening socket
	"dialog_list": 			("dialog_list", [args.NonNegativeNumber("limit", optional=True, default=100), args.NonNegativeNumber("offset", optional=True, default=0)], res.success_fail, None),  # List of last conversations
	"set_password": 		("set_password", [args.UnicodeString("hint", optional=True, default="empty")], res.success_fail, None),  # Sets password

	# diversa
	"raw": 					("", 					[args.UnescapedUnicodeString("command")], res.raw, None), # just send custom shit to the cli. Use, if there are no fitting functions, because I didn't update.
	"help": 				("help", [], res.raw, None),  # Prints the help. (Needed for pytg itself!)

	# these are commented out in the cli too:

	#//"reply_text": ("reply_text", [args.MsgId("msg_id"), ca_number, ca_file_name_end, ca_none,"<msg-id> <file>"], res.success_fail, None),  # Sends contents of text file as plain text message
	#//"restore_msg": ("restore_msg", [args.MsgId("msg_id"), ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Restores message. Only available shortly (one hour?) after deletion
	#//"secret_chat_rekey": ("secret_chat_rekey", [args.SecretChat("secret_chat")], res.success_fail, None),  # generate new key for active secret chat
	#"set": ("set", [ca_string, ca_number, ca_none,"<param> <value>"], res.success_fail, None),  # Sets value of param. Currently available: log_level, debug_verbosity, alarm, msg_num

	#These are not concidered useful, so I implement other things first. If needed, create an issue, or send an pull-request.

	#"show_license": ("show_license", [ca_none,""], res.success_fail, None),  # Prints contents of GPL license
	#"stats": ("stats", [ca_none,""], res.success_fail, None),  # For debug purpose
	#"view_audio": ("view_audio", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_chat_photo": ("view_chat_photo", [ca_chat, ca_none,"<chat>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_document": ("view_document", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_document_thumb": ("view_document_thumb", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_file": ("view_file", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_file_thumb": ("view_file_thumb", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_photo": ("view_photo", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_user_photo": ("view_user_photo", [ca_user, ca_none,"<user>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_video": ("view_video", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view_video_thumb": ("view_video_thumb", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Downloads file to downloads dirs. Then tries to open it with system default action
	#"view": ("view", [ca_number, ca_none,"<msg-id>"], res.success_fail, None),  # Tries to view message contents

}
# regex to transform the C function list of the CLI to the one for pytg (in Python, obviously)
##^\s*(?://)?\s*\{"(.*?)", \{\s*((?:ca_(?:[a-z_A-Z]+)(?:(?:,|\s+\|)\s+)?)+)\},\s+[a-z_A-Z]+,\s+"(?:(?:\1\s*(.*?)\\t)?)(.+?)",\s+NULL}(,?)$##
#  replace with:
##\t"$1": ("$1", [$2,"$3"], res.success_fail, None)$5  # $4##


_ANSWER_SYNTAX = b("ANSWER ")
_LINE_BREAK = b("\n")

class Sender(object):
	_do_quit = False
	default_answer_timeout = 1.0 # how long it should wait for a answer. DANGER: if set to None it will block!

	def __init__(self, host, port):
		"""

		:param host:
		:param port:
		:param answer_timeout: how long it waits for the cli to answer, a float in seconds. Note that that commands like send_msg will not return anything, so a timeout makes sense to continue anyway.
		:return:
		"""
		self.s = None
		self.host = host
		self.port_out = port
		self.debug = False
		self._socked_used = threading.Semaphore(1)  # start unblocked.
		atexit.register(self.terminate)
		self._register_all_functions()

	def execute_function(self, function_name, *arguments, **kwargs):
		"""
		Execute a function.
		:param function_name:
		:param arguments:
		:param retry_connect=2:  How often it should try to reconnect (-1 = infinite times) or fail if it can't establish the first connection.
		:return: parsed result/exception
		"""
		command_name, new_args = self._validate_input(function_name, arguments)
		retry_connect = 2 #default value
		if "retry_connect" in kwargs:
			retry_connect = kwargs["retry_connect"]
		if self._do_quit and not "quit" in command_name:
			raise AssertionError("Socket already terminated.")
		result_parser = functions[function_name][FUNC_RES]
		result_timeout = functions[function_name][FUNC_TIME]
		try:
			if result_timeout:
				result = self._do_command(command_name, *new_args, answer_timeout=result_timeout, retry_connect=retry_connect)
			else:
				result = self._do_command(command_name, *new_args, answer_timeout=self.default_answer_timeout, retry_connect=retry_connect)
		except ConnectionError as err:
			raise
		except NoResponse as err:
			args_ = inspect.getargspec(result_parser)[0]
			if not "exception" in args_:
				logger.exception("Result parser does not allow exceptions, but we got one: ")
				raise IllegalResponseException("Result parser does not allow exceptions.")
			try:
				return_result = result_parser(exception=err)
				return return_result
			except TypeError:
				logger.error("Result parser did not allow exceptions.")
				raise
		if result_parser != res.raw: # skip json'ing stuff marked as raw output.
			try:
				json_dict = json.loads(result)
				message = DictObject.objectify(json_dict)
				message = fix_message(message)
			except:
				logger.exception("Parsing of answer failed, maybe not valid json?\nMessage: >{}<".format(result))
				result_parser
				return IllegalResponseException("Parsing of answer failed, maybe not valid json?\nMessage: >{}<".format(result))  #TODO: This is *very* bad code.
			return result_parser(message)
		return result_parser(result) # raw()


	@staticmethod
	def _validate_input(function_name, arguments):
		"""
		:rtype : (srt, list)
		"""
		if not function_name in functions:
			raise UnknownFunction(function_name)
		command_name    = functions[function_name][FUNC_CMD]
		arguments_types = functions[function_name][FUNC_ARGS]
		""":type arguments_types: list of pytg.argument_types.Argument"""
		if len(arguments) > len(arguments_types):
			raise ValueError(
				"Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(
					function_name=function_name, expected_number=len(arguments_types), given_number=len(arguments))
			)
		#end if
		i = 0
		new_args = []
		error = None
		for func_type in arguments_types:
			""":type func_type: pytg.argument_types.Argument"""
			if i >= len(arguments): # if to many arguments
				if not func_type.optional:
					raise ValueError(
						"Error in function {function_name}: Not enough parameter given, {arg_name} missing. Arguments got: {arguments}".format(
							function_name=function_name, arguments=arguments, arg_name=str(func_type))
					)
				else:
					logger.debug("Skipping missing optional parameter #{number} {arg_name} (type {type}) in function {function_name}.".format(
						type=func_type.__class__.__name__, function_name=function_name,  number=i, arg_name=str(func_type))
					)
					continue  # do not increment i, we are still processing the same arg.
				#end if optional
			#end if to many arguments
			arg = arguments[i]
			logger.debug("Parsing {function_name}: Argument {arg} - {type} ({opt})".format(function_name=function_name, arg=arg, type=str(func_type), opt=("optional" if hasattr(func_type, "_optional") else "needed")))
			# arg is the given one, which should be func_type.

			arg_value = None
			try:
				arg_value = func_type.parse(arg)
			except Exception as err:
				logger.debug("Got error", exc_info=True)
				if func_type.optional:
					logger.debug("Skipping unfitting optional parameter #{number} {param} (type {type}) in function {function_name}.".format(type=func_type.__class__.__name__, function_name=function_name, param=str(func_type),  number=i))
					continue  # do not increment i, we are still processing the same arg.
				raise ValueError("Error in function {function_name}: parameter #{number} {param} is not type {type}. ({error})".format(
					function_name=function_name, number=i, type=func_type.__class__.__name__, param=str(func_type), error=str(err)))
			new_args.append(u(str(arg_value)))
			i += 1
		return command_name, new_args

	#def __getattr__(self, attr):
	#	if attr in functions:
	#		command = self.Command(attr, self)
	#		setattr(self, attr, command)
	#		return command
	#	else:
	#		return object.__getattribute__(self, attr)

	def _do_command(self, function_sting, *argmts, **kwargs):
		arg_string = " ".join([u(x) for x in argmts])
		request = " ".join([function_sting,  arg_string])
		request = "".join([request, "\n"]) #TODO can this be deleted?
		result = self._do_send(request, **kwargs)
		return result

	class Command:
		def __init__(self, name, sender_instance):
			self.name = name
			self.sender_instance = sender_instance

		def __call__(self, *args, **kwargs):
			return self.sender_instance.execute_function(self.name, *args, **kwargs)

	def _do_send(self, command, answer_timeout=default_answer_timeout, retry_connect=2):
		"""
		You can force retry with retry_connect=2 (3 tries, default settings, first try + 2 retries)
		retry_connect=0 , retry_connect=False and retry_connect=None  means not to retry,
		retry_connect=True or retry_connect= -1 means to retry infinite times.

		:type command: builtins.str
		:type answer_timeout: builtins.float or builtins.int
		:param retry_connect:
		:return:
		"""
		if isinstance(retry_connect, int):
			pass # correct
		elif isinstance(retry_connect, bool):
			if retry_connect: # True = forever
				retry_connect = -1
			else:
				retry_connect = 0
		elif retry_connect is None:
			retry_connect = 0
		else:
			raise ValueError("retry_connect is not type int, bool or None.")
		retry_connect_original = retry_connect

		if not isinstance(command, (text_type, binary_type)):
			raise TypeError("Command to send is not a unicode(?) string. (Instead of %s you used %s.) " % (str(text_type), str(type(command))))
		logger.debug("Sending command >%s<" % n(command))
		with self._socked_used:
			while not self._do_quit:
				if self.s:
					self.s.close()
					self.s = None
				self.s = socket.socket()
				try:
					self.s.connect((self.host, self.port_out))
				except socket_error as error:
					self.s.close()
					if error.errno == ECONNREFUSED and not self._do_quit:
						if retry_connect != 0:
							sleep(1)
							if retry_connect > 0:
								retry_connect -= 1
							continue
						else:
							raise ConnectionError("Could not establish connection to the cli port, failed after {number} tries. (called with retry_connect={retry_connect})".format(number=(retry_connect_original+1), retry_connect=retry_connect_original))
					raise error  # Not the error we are looking for, re-raise
				except Exception as error:
					self.s.close()
					raise error
				logger.debug("Socket Connected.")
				try:
					self.s.sendall(b(command))
				except Exception as error:
					self.s.close()
					raise error #retry?
				logger.debug("All Sent.")
				completed = -1 # -1 = answer size yet unknown, >0 = got remaining answer size
				buffer = b("")
				self.s.settimeout(answer_timeout) # in seconds.
				while completed != 0:
					try:
						while 1: #retry if CTRL+C'd
							try:
								answer = self.s.recv(1)
								# recv() returns an empty string if the remote end is closed
								if len(answer) == 0:
									raise ConnectionError("Remote end closed")
								break
							except socket_error as err:
								if err.errno != EINTR:
									raise
								else:
									logger.exception("Uncatched exception in reading answer from cli.")
						self.s.settimeout(max(self.default_answer_timeout, answer_timeout)) # in seconds.
						# If there was input the input is now either the default one or the given one, which waits longer.
						buffer += answer
						if completed < -1 and buffer[:len(_ANSWER_SYNTAX)] != _ANSWER_SYNTAX[:len(buffer)]:
							raise ArithmeticError("Server response does not fit.")
						if completed <= -1 and buffer.startswith(_ANSWER_SYNTAX) and buffer.endswith(_LINE_BREAK):
							completed = int(n(buffer[7:-1])) #TODO regex.
							buffer = b("")
						completed -= 1
					except ConnectionError:
						self.s.close()
						raise
					except socket.timeout:
						raise NoResponse(command)
					except KeyboardInterrupt as error:
						logger.exception("Exception while reading the Answer for \"%s\". Got so far: >%s< of %i\n" % (n(command), n(buffer), completed))  # TODO remove me
						self.s.close()
						raise
					except Exception as error:
						logger.exception("Exception while reading the Answer for \"%s\". Got so far: >%s<\n" % (n(command), n(buffer))) #TODO remove me
						self.s.close()
						raise
						#raise error
				# end while completed != 0
				if self.s:
					self.s.close()
					self.s = None
				return u(buffer)
			# end while not self._do_quit
		# end with lock
		if self.s:
			self.s.close()
	# end of function

	def stop(self):
		if self._do_quit:
			logger.debug("Already did quit Sending. Not allowing sending.")
		else:
			logger.info("Quit Sending. Not allowing sending anymore.")
			self._do_quit = True
	def unstop(self):
		if self._do_quit:
			logger.info("Unquit Sending. Allowing sending again.")
			self._do_quit = False
		else:
			logger.debug("Already did unquit Sending. Allowing sending.")
		logger.info("Unquit Sending. Allowing sending again.")

	def terminate(self):
		self.stop()
		logger.warn("Terminating currently sending request.")
		if self._socked_used.acquire(blocking=False):
			# Nothing is going on, just quit then.
			logger.info("Currently not Sending.")
			self._socked_used.release() # someone can use it again.
			return
		else:
			# Something was using the socket for more than 15 seconds.
			logger.warn("Aborting Sending.")
			if self.s:
				#self.s.settimeout(0)
				self.s.close()  # not let the cli end close first -> avoid bind: port already in use.
			return # don't abort sending, let it do stuff, it will suceed or fail soon anyway.
			#	   # Well, hopefully. Else something like this should work:
			#if self.s:
			#	self.s.close()

#class Sender(object): pass
def _register_all_functions():
	if hasattr(Sender, "did_register_all_functions"):
		raise AssertionError("Sender class already did register all custom functions.")
	setattr(Sender, "did_register_all_functions", True)
	for function, meta in functions.items():  # slow in python 2:  http://stackoverflow.com/a/3294899
		def command_alias(self, *args, **kwargs):
			self.sender_instance.execute_function(self._name, *args, **kwargs)
		command_alias._name = function
		arguments = []
		cli_args = []
		args_description = []
		for current_arg in meta[FUNC_ARGS]:
			assert isinstance(current_arg, args.Argument)
			arguments.append(current_arg.name)
			cli_args.append(str(current_arg))
			args_description.append("`{arg_name}`: {optional}, needs a {arg_class} (type: {type}), and may {allow_multible} be repeated.".format(arg_name=current_arg.name,
									optional="optional" if current_arg.optional else "mandatory",
									arg_class=current_arg.__class__.__name__,
									allow_multible="not" if not current_arg.multible else "",
									type=current_arg.type))
		if len(args_description) == 0:
			argument_description = "No arguments."
		else:
			argument_description = "Arguments:\n{args_description}".format(args_description="\n".join(args_description))
		docstring = "Function to interact with the cli.\n\n" \
					"`def {func_name}({arguments})`\n\n" \
					"{argument_description}\n" \
					"# will be send to the cli as `{cli_command}{cli_args}`".format(func_name=function, arguments=", ".join(arguments), cli_args=" ".join(cli_args), cli_command=meta[FUNC_CMD] + (" " if len(cli_args)>0 else ""), argument_description=argument_description)
		set_docstring(command_alias, docstring)
		setattr(Sender, function, command_alias)

_register_all_functions()

#help(Sender)
