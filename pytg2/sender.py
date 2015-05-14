__author__ = 'luckydonald'
from . import result_parser as res
from . import argument_types as args
from .utils import escape
from .encoding import to_native as n
from .encoding import to_unicode as u
from .encoding import to_binary as b
from .encoding import text_type, binary_type
from .exceptions import UnknownFunction, ConnectionError, NoResponse, IllegalResponseException
from .argument_types import Argument
from .msg_array_fixer import fix_message

import json
from DictObject import DictObject
import socket # connect to telegram cli.
from errno import ECONNREFUSED, EINTR
from socket import error as socket_error
import threading
import atexit
import inspect # g
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
	"get_dialog_list": 		["dialog_list", 		[args.PositiveNumber("limit", optional=True), args.NonNegativeNumber("offset", optional=True)], res.something, 	None],
	"rename_chat": 			["rename_chat", 		[args.Chat("chat"), args.UnicodeString("new_name")],			res.success_fail, None],
	"send_msg": 			["msg", 				[args.Peer("peer"), args.UnicodeString("test")],				res.success_fail, None],
	"send_typing": 			["send_typing", 		[args.Peer("peer")],							res.success_fail, None],
	"send_typing_abort": 	["send_typing_abort", 	[args.Peer("peer")],													res.success_fail, None],
	"send_photo": 			["send_photo", 			[args.Peer("peer"), args.File("file"), args.UnicodeString("caption", optional=True)],											res.success_fail, 60.0],
	"send_video": 			["send_video", 			[args.Peer("peer"), args.File("file"), args.UnicodeString("caption", optional=True)],											res.success_fail, 60.0],
	"send_audio": 			["send_audio", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0],
	"send_document": 		["send_document", 		[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0],
	"send_file": 			["send_file", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0],
	"send_text": 			["send_text", 			[args.Peer("peer"), args.File("file")],											res.success_fail, 60.0],
	"send_location": 		["send_location", 		[args.Peer("peer"), args.Double("latitude"), args.Double("longitude")],							res.success_fail, None],
	"load_photo": 			["load_photo", 			[args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"load_video": 			["load_video", 			[args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"load_video_thumb": 	["load_video_thumb", 	[args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"load_audio": 			["load_audio", 			[args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"load_document": 		["load_document", 		[args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"load_document_thumb": 	["load_document_thumb", [args.MsgId("msg_id")],													res.something, 	60.0], #String saying something and a filepath
	"fwd_msg": 				["fwd",		 			[args.Peer("peer"), args.MsgId("msg_id")],										res.success_fail, None],
	"fwd_media": 			["fwd_media", 			[args.Peer("peer"), args.MsgId("msg_id")],										res.success_fail, None],
	"chat_info": 			["chat_info", 			[args.Chat("chat")],													res.something, None],
	"chat_set_photo": 		["chat_set_photo", 		[args.Chat("chat"), args.File("file")],								res.success_fail, None],
	"chat_add_user": 		["chat_add_user", 		[args.Chat("chat"), args.User("user"), args.NonNegativeNumber("msgs_to_forward", optional=True)],	res.something, 	60.0],
	"chat_del_user": 		["chat_del_user", 		[args.Chat("chat"), args.User("user")],											res.success_fail, None],
	"create_secret_chat": 	["create_secret_chat", 	[args.User("user")],													res.success_fail, None],
	"create_group_chat": 	["create_group_chat", 	[args.UnicodeString("name"), args.User("user", multible=True)],								res.success_fail, None],
	"user_info": 			["user_info", 			[args.User("user")],													res.something, None],
	"get_history": 			["history", 			[args.Peer("user"), args.PositiveNumber("limit", optional=True), args.NonNegativeNumber("offset", optional=True)],							res.something, None],
	"add_contact": 			["add_contact", 		[args.UnicodeString("phone"), args.UnicodeString("first_name"), args.UnicodeString("last_name")], res.something, None], #returns the new name
	"rename_contact": 		["rename_contact", 		[args.User("user"), args.UnicodeString("first_name"), args.UnicodeString("last_name")],			res.something, None], #returns the new name
	"del_contact": 			["del_contact", 		[args.User("user")],													res.success_fail, None],
	"msg_search": 			["search", 				[
														args.Peer("peer", optional=True),
														args.NonNegativeNumber("limit", optional=True),
														args.NonNegativeNumber("from", optional=True),
														args.NonNegativeNumber("to", optional=True),
														args.NonNegativeNumber("offset", optional=True),
														args.UnicodeString("pattern")
													],							res.something, None],
	"mark_read": 			["mark_read", 			[args.Peer("peer")],													res.success_fail, None],
	"set_profile_photo": 	["set_profile_photo", 	[args.File("file")],													res.something, 	60.0], #TODO
	"set_profile_name": 	["set_profile_name", 	[args.UnicodeString("first_name"), args.UnicodeString("last_name")],	res.something, 	60.0], #ret: new name
	"delete_msg": 			["delete_msg", 			[args.MsgId("msg_id")],													res.success_fail, None],
	"accept_secret_chat": 	["accept_secret_chat", 	[args.SecretChat("secret_chat")],												res.success_fail, None],
	"send_contact": 		["send_contact", 		[args.Peer("peer"), args.UnicodeString("phone"), args.UnicodeString("first_name"), args.UnicodeString("last_name")], res.something, 	60.0], #ret: formated message
	"status_online": 		["status_online", 		[],																res.success_fail, None],
	"status_offline": 		["status_offline", 		[],																res.success_fail, None],
	"quit": 				["quit", 				[],																res.response_fails, None],
	"safe_quit": 			["safe_quit",	 		[],																res.response_fails, None],
	"raw": 					["", 					[args.UnescapedUnicodeString],								res.anything, None]
} 	# \{"(.*)",\ .*,\ \{\ (.*)\ \}\}, >> "$1": ["$1", [$2]],


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


	def execute_function(self, function_name, *arguments):
		"""
		Execute a function.
		:param function_name:
		:param arguments:
		:param answer_timeout:  set to a float to set a custom timeout for this answer.
		:return: parsed result/exception
		"""
		command_name, new_args = self._validate_input(function_name, arguments)
		if self._do_quit and not "quit" in command_name:
			raise AssertionError("Socket already terminated.")
		result_parser = functions[function_name][FUNC_RES]
		result_timeout = functions[function_name][FUNC_TIME]
		try:
			if result_timeout:
				result = self._do_command(command_name, *new_args, answer_timeout=result_timeout)
			else:
				result = self._do_command(command_name, *new_args, answer_timeout=self.default_answer_timeout)
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
		try:
			json_dict = json.loads(result)
			message = DictObject.objectify(json_dict)
			message = fix_message(message)
		except:
			logger.exception("Parsing of answer failed, maybe not valid json?\nMessage: >{}<".format(result))
			return IllegalResponseException("Parsing of answer failed, maybe not valid json?\nMessage: >{}<".format(result))  #TODO: This is *very* bad code.
		return result_parser(message)

	@staticmethod
	def _validate_input(function_name, arguments):
		"""
		:rtype : (srt, list)
		"""
		if not function_name in functions:
			raise UnknownFunction(function_name)
		command_name    = functions[function_name][FUNC_CMD]
		arguments_types = functions[function_name][FUNC_ARGS]
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
			""":type func_type: Argument"""
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
					self.s = None
				self.s = socket.socket()
				try:
					self.s.connect((self.host,self.port_out))
				except socket_error as error:
					self.s.close()
					if error.errno == ECONNREFUSED and not self._do_quit:
						continue
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
				self.s.settimeout(0)
			return # don't abort sending, let it do stuff, it will suceed or fail soon anyway.
			#	   # Well, hopefully. Else something like this should work:
			#if self.s:
			#	self.s.close()