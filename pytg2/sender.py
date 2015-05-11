from pytg2.argumenttypes import UnknownFunction

__author__ = 'luckydonald'
from . import argumenttypes as args
from . import result_parser as res
from .utils import escape
from .encoding import to_native as n
from .encoding import to_unicode as u
from .encoding import to_binary as b
from .encoding import text_type, binary_type
import socket # connect to telegram cli.
from errno import ECONNREFUSED, EINTR
from socket import error as socket_error
import threading
import atexit
import logging
logger = logging.getLogger(__name__)

SOCKET_SIZE = 1 << 25

FUNC_CMD  = 0
FUNC_ARGS = 1
FUNC_RES  = 2
FUNC_TIME = 3
__all__ = ["FUNC_CMD", "FUNC_ARGS", "FUNC_RES", "functions", "Sender", "NoResponse"]
functions = {
	# function to call      # actual telegram command  # required arguments  # expected return type (parser)  # timeout (None = global default)
	"get_contact_list":		["contact_list",		[],																res.something, 	None],
	"get_dialog_list": 		["dialog_list", 		[],																res.something, 	None],
	"rename_chat": 			["rename_chat", 		[args.chat, args.unicode_string],								res.success_fail, None],
	"send_msg": 			["msg", 				[args.peer, args.unicode_string],								res.success_fail, None],
	"send_typing": 			["send_typing", 		[args.peer, args.nonnegative_number],							res.success_fail, None],
	"send_typing_abort": 	["send_typing_abort", 	[args.peer],													res.success_fail, None],
	"send_photo": 			["send_photo", 			[args.peer, args.file],								res.success_fail, 60.0],
	"send_video": 			["send_video", 			[args.peer, args.file],								res.success_fail, 60.0],
	"send_audio": 			["send_audio", 			[args.peer, args.file],								res.success_fail, 60.0],
	"send_document": 		["send_document", 		[args.peer, args.file],								res.success_fail, 60.0],
	"send_file": 			["send_file", 			[args.peer, args.file],								res.success_fail, 60.0],
	"send_text": 			["send_text", 			[args.peer, args.file],								res.success_fail, 60.0],
	"send_location": 		["send_location", 		[args.peer, args.double, args.double],							res.success_fail, None],
	"load_photo": 			["load_photo", 			[args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"load_video": 			["load_video", 			[args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"load_video_thumb": 	["load_video_thumb", 	[args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"load_audio": 			["load_audio", 			[args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"load_document": 		["load_document", 		[args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"load_document_thumb": 	["load_document_thumb", [args.msg_id],													res.something, 	60.0], #String saying something and a filepath
	"fwd_msg": 				["fwd",		 			[args.peer, args.msg_id],										res.success_fail, None],
	"fwd_media": 			["fwd_media", 			[args.peer, args.msg_id],										res.success_fail, None],
	"chat_info": 			["chat_info", 			[args.chat],													res.something, None],
	"chat_set_photo": 		["chat_set_photo", 		[args.chat, args.unicode_string],								res.success_fail, None],
	"chat_add_user": 		["chat_add_user", 		[args.chat, args.user],											res.something, 	60.0],
	"chat_del_user": 		["chat_del_user", 		[args.chat, args.user],											res.success_fail, None],
	"create_secret_chat": 	["create_secret_chat", 	[args.user],													res.success_fail, None],
	"create_group_chat": 	["create_group_chat", 	[args.unicode_string, args.user],								res.success_fail, None],
	"user_info": 			["user_info", 			[args.user],													res.something, None],
	"get_history": 			["history", 			[args.peer, args.nonnegative_number],							res.something, None],
	"add_contact": 			["add_contact", 		[args.unicode_string, args.unicode_string, args.unicode_string],res.something, None], #returns the new name
	"rename_contact": 		["rename_contact", 		[args.user, args.unicode_string, args.unicode_string],			res.something, None], #returns the new name
	"del_contact": 			["del_contact", 		[args.user],													res.success_fail, None],
	"msg_search": 			["search", 				[args.peer, args.unicode_string],								res.something, None], #ret: formated messages
	"msg_global_search": 	["search", 				[args.unicode_string],											res.something, None], #ret: formated messages
	"mark_read": 			["mark_read", 			[args.peer],													res.success_fail, None],
	"set_profile_photo": 	["set_profile_photo", 	[args.file],											res.something, 	60.0], #TODO
	"set_profile_name": 	["set_profile_name", 	[args.unicode_string, args.unicode_string],						res.something, 	60.0], #ret: new name
	"delete_msg": 			["delete_msg", 			[args.msg_id],													res.success_fail, None],
	"restore_msg": 			["restore_msg", 		[args.positive_number],											res.success_fail, None],
	"accept_secret_chat": 	["accept_secret_chat", 	[args.secret_chat],												res.success_fail, None],
	"send_contact": 		["send_contact", 		[args.peer, args.unicode_string, args.unicode_string, args.unicode_string], res.something, 	60.0], #ret: formated message
	"status_online": 		["status_online", 		[],																res.success_fail, None],
	"status_offline": 		["status_offline", 		[],																res.success_fail, None],
	"quit": 				["quit", 				[],																res.success_fail, None],
	"safe_quit": 			["safe_quit",	 		[],																res.success_fail, None],
	"raw": 					["", 					[args.unescaped_unicode_string],								res.anything, None]
} 	# \{"(.*)",\ .*,\ \{\ (.*)\ \}\}, >> "$1": ["$1", [$2]],


_ANSWER_SYNTAX = b("ANSWER ")
_LINE_BREAK = b("\n")

class Sender(object):
	_do_quit = False
	default_answer_timeout = 0.2 # how long it should wait for a answer. DANGER: if set to None it will block!
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


	def execute_function(self, function_name, *arguments):
		"""
		Execute a function.
		:param function_name:
		:param arguments:
		:param answer_timeout:  set to a float to set a custom timeout for this answer.
		:return:
		"""
		command_name, new_args = self._validate_input(function_name, arguments)
		if self._do_quit and not "quit" in command_name:
			raise AssertionError("Socket already terminated.")
		result_parser = functions[function_name][FUNC_RES]
		result_timeout = functions[function_name][FUNC_TIME]
		if result_timeout:
			result = self._do_command(command_name, *new_args, answer_timeout = result_timeout)
		else:
			result = self._do_command(command_name, *new_args, answer_timeout = self.default_answer_timeout)

		return result_parser(result)

	@staticmethod
	def _validate_input(function_name, arguments):
		"""
		:rtype : (srt, list)
		"""
		if not function_name in functions:
			raise UnknownFunction(function_name)
		command_name    = functions[function_name][FUNC_CMD]
		arguments_types = functions[function_name][FUNC_ARGS]
		if len(arguments) != len(arguments_types):
			raise ValueError(
				"Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(
					function_name=function_name, expected_number=len(arguments_types), given_number=len(arguments))
			)
		#end if
		i = 0
		new_args = []
		for arg in arguments:
			func_type = arguments_types[i]
			# arg is the given one, which should be func_type.
			if not func_type(arg):
				raise ValueError("Error in function {function_name}: parameter {number} is not type {type}.".format(
					function_name=function_name, number=i, type=func_type.__name__))
			if func_type == args.unicode_string:
				new_args.append(u(escape(arg)))
			else:
				new_args.append(u(str(arg)))
			i += 1
		return command_name, new_args

	def __getattr__(self, attr):
		if attr in functions:
			command = self.Command(attr, self)
			setattr(self, attr, command)
			return command
		else:
			return object.__getattribute__(self, attr)

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

		def __call__(self, *args):
			return self.sender_instance.execute_function(self.name, *args)

	def _do_send(self, command, answer_timeout=default_answer_timeout):
		if not isinstance(command, (text_type, binary_type)):
			raise TypeError("Command to send is not a unicode(?) string. (Instead of %s you used %s.) " % (str(text_type), str(type(command))))
		logger.debug("Sending command >%s<" % n(command))
		with self._socked_used:
			while not self._do_quit:
				if self.s:
					self.s.close()
					del self.s
				self.s = socket.socket()
				try:
					self.s.connect((self.host,self.port_out))
				except socket_error as error:
					self.s.close()
					if error.errno != ECONNREFUSED:
						raise error  # Not the error we are looking for, re-raise
					continue
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
								break
							except socket_error as err:
								if err.errno != EINTR:
									raise
						self.s.settimeout( max(self.default_answer_timeout, answer_timeout) ) # in seconds.
						# If there was input the input is now either the default one or the given one, which waits longer.
						buffer += answer
						if completed < -1 and buffer[:len(_ANSWER_SYNTAX)] != _ANSWER_SYNTAX[:len(buffer)]:
							raise ArithmeticError("Server response does not fit.")
						if completed <= -1 and buffer.startswith(_ANSWER_SYNTAX) and buffer.endswith(_LINE_BREAK):
							completed = int(n(buffer[7:-1])) #TODO regex.
							buffer = b("")
						completed -= 1
					except socket.timeout:
						raise NoResponse(command)
					except KeyboardInterrupt as error:
						logger.error("Exception while reading the Answer for \"%s\". Got so far: >%s< of %i\n" % (n(command),n(buffer),completed))  # TODO remove me
						self.s.close()
						raise
					except Exception as error:
						logger.error("Exception while reading the Answer for \"%s\". Got so far: >%s<\n" % (n(command),n(buffer))) #TODO remove me
						self.s.close()
						raise
						#raise error
				# end while completed != 0
				if self.s:
					self.s.close()
				return u(buffer)
			# end while not self._do_quit
		# end with lock
		if self.s:
			self.s.close()
	# end of function

	def terminate(self):
		self._do_quit = True
		if self._socked_used.acquire(blocking=False):
			# Nothing is going on, just quit then.
			logger.info("Stopped Sending.")
			self._socked_used.release()
			return
		else:
			# Something was using the socket for more than 15 seconds.
			logger.warn("Aborting Sending.")
			if self.s:
				self.s.settimeout(0)
			return # don't abort sending, let it do stuff, it will suceed or fail soon anyway.
				   # Well, hopefully. Else something like this should work:
			#if self.s:
			#	self.s.close()



class NoResponse(Exception):
	pass