__author__ = 'luckydonald'
from . import argumenttypes as args
from . import result_parser as res
from .utils import suppress_context, escape
from .encoding import to_native as n
from .encoding import to_unicode as u
from .encoding import to_binary as b
from .encoding import text_type, binary_type
import socket # connect to telegram cli.
from errno import ECONNREFUSED
from socket import error as socket_error
import threading

SOCKET_SIZE = 1 << 25

FUNC_CMD  = 0
FUNC_ARGS = 1
FUNC_RES  = 2
__all__ = ["FUNC_CMD", "FUNC_ARGS", "FUNC_RES", "functions", "Sender"]
functions = {
	"get_contact_list":		["contact_list",		[],																],
	"get_dialog_list": 		["dialog_list", 		[],																],
	"rename_chat": 			["rename_chat", 		[args.chat, args.unicode_string],								],
	"send_msg": 			["msg", 				[args.peer, args.unicode_string],								res.success_fail],
	"send_typing": 			["send_typing", 		[args.peer, args.nonnegative_number],							],
	"send_typing_abort": 	["send_typing_abort", 	[args.peer],													],
	"send_photo": 			["send_photo", 			[args.peer, args.unicode_string],								],
	"send_video": 			["send_video", 			[args.peer, args.unicode_string],								],
	"send_audio": 			["send_audio", 			[args.peer, args.unicode_string],								],
	"send_document": 		["send_document", 		[args.peer, args.unicode_string],								],
	"send_file": 			["send_file", 			[args.peer, args.unicode_string],								],
	"send_text": 			["send_text", 			[args.peer, args.unicode_string]								],
	"send_location": 		["send_location", 		[args.peer, args.double, args.double],							],
	"load_photo": 			["load_photo", 			[args.msg_id],													],
	"load_video": 			["load_video", 			[args.msg_id],													],
	"load_video_thumb": 	["load_video_thumb", 	[args.msg_id],													],
	"load_audio": 			["load_audio", 			[args.msg_id],													],
	"load_document": 		["load_document", 		[args.msg_id],													],
	"load_document_thumb": 	["load_document_thumb", [args.msg_id],													],
	"fwd_msg": 				["fwd",		 			[args.peer, args.msg_id],										],
	"fwd_media": 			["fwd_media", 			[args.peer, args.msg_id],										],
	"chat_info": 			["chat_info", 			[args.chat],													],
	"chat_set_photo": 		["chat_set_photo", 		[args.chat, args.unicode_string],								],
	"chat_add_user": 		["chat_add_user", 		[args.chat, args.user],											],
	"chat_del_user": 		["chat_del_user", 		[args.chat, args.user],											],
	"create_secret_chat": 	["create_secret_chat", 	[args.user],													],
	"create_group_chat": 	["create_group_chat", 	[args.user, args.unicode_string],								],
	"user_info": 			["user_info", 			[args.user],													],
	"get_history": 			["history", 			[args.peer, args.nonnegative_number],							],
	"add_contact": 			["add_contact", 		[args.unicode_string, args.unicode_string, args.unicode_string],],
	"del_contact": 			["del_contact", 		[args.user],													],
	"rename_contact": 		["rename_contact", 		[args.unicode_string, args.unicode_string, args.unicode_string],],
	"msg_search": 			["search", 				[args.peer, args.unicode_string],								],
	"msg_global_search": 	["search", 				[args.unicode_string],											],
	"mark_read": 			["mark_read", 			[args.peer],													],
	"set_profile_photo": 	["set_profile_photo", 	[args.unicode_string],											],
	"set_profile_name": 	["set_profile_name", 	[args.unicode_string],											],
	"delete_msg": 			["delete_msg", 			[args.msg_id],													],
	"restore_msg": 			["restore_msg", 		[args.positive_number],											],
	"accept_secret_chat": 	["accept_secret_chat", 	[args.secret_chat],												],
	"send_contact": 		["send_contact", 		[args.peer, args.unicode_string, args.unicode_string, args.unicode_string],],
	"status_online": 		["status_online", 		[],																],
	"status_offline": 		["status_offline", 		[],																],
	"quit": 				["quit", 				[],																],
	"safe_quit": 			["safe_quit",	 		[],																],
	"raw": 					["", 					[args.unescaped_unicode_string],								]
} 	# \{"(.*)",\ .*,\ \{\ (.*)\ \}\}, >> "$1": ["$1", [$2]],


class DelayedFunctions():
		def __init__(self, function_name, *arguments):
			self.function_name = function_name
			self.args = args
_ANSWER_SYNTAX = b("ANSWER ")
_LINE_BREAK = b("\n")
class Sender(object):
	def __init__(self, host, port):
		self.host = host
		self.port_out = port
		self.debug = False
		self._socked_used = threading.Semaphore(1)  # start unblocked.


	def execute_function(self, function_name, *arguments):
		arguments_types = functions[function_name][FUNC_ARGS]
		command_name = functions[function_name][FUNC_CMD]
		if (len(arguments) != len(arguments_types)):
			raise ValueError("Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(function_name=function_name, expected_number=len(arguments_types), given_number=len(args)))
		i = 0
		new_args = []
		for arg in arguments:
			func_type = arguments_types[i]
			# arg is the given one, which should be func_type.
			if not func_type(arg):
				raise ValueError("Error in function {function_name}: parameter {number} is not type {type}.".format(function_name=function_name, number=i, type=func_type.__name__))
			if func_type == args.unicode_string:
				new_args.append(u(escape(arg)))
			else:
				new_args.append(u(str(arg)))
			i += 1
		# end for
		return self._do_command(command_name, *new_args)

	def __getattr__(self, attr):
		if attr in functions:
			#print("newly: %s" % attr)
			command = self.Command(attr, self)
			setattr(self, attr, command)
			return command
		else:
			return object.__getattribute__(self, attr)

	def _do_command(self, function_sting, *argmts):
		arg_string = " ".join([str(x) for x in argmts])
		request = " ".join([function_sting,  arg_string])
		request = "".join([request, "\n"]) #TODO can this be deleted?
		result = self._do_send(request)
		return result

	class Command:
		def __init__(self, name, sender_instance):
			self.name = name
			self.sender_instance = sender_instance

		def __call__(self, *args):
			return self.sender_instance.execute_function(self.name, *args)

	def _do_send(self, command):
		if not isinstance(command, (text_type, binary_type)):
			raise TypeError("Command to send is not a unicode(?) string. (Instead of %s you used %s.) " % (str(text_type), str(type(command))))
		if self.debug:
			print("Sending command >%s<" % n(command))
		s = None
		with self._socked_used:
			while 1:
				if s:
					s.close()
					del s
				s = socket.socket()
				try:
					s.connect((self.host,self.port_out))
				except socket_error as error:
					s.close()
					if error.errno != ECONNREFUSED:
						raise socket_error  # Not the error we are looking for, re-raise
					continue
				except Exception as error:
					s.close()
					raise error
				if self.debug:
					print("Connected.")
				try:
					s.send(b(command))
				except Exception as error:
					s.close()
					raise error #retry?
				if self.debug:
					print("Sended.")
				completed = -1 # -1 = answer size yet unknown, >0 = got remaining answer size
				buffer = b("")
				while completed != 0:
					try:
						s.settimeout(10) # in seconds.
						answer = s.recv(1)
						buffer += answer
						if completed < -1 and buffer[:len(_ANSWER_SYNTAX)] != _ANSWER_SYNTAX[:len(buffer)]:
							raise ArithmeticError("Server response does not fit.")
						if completed <= -1 and buffer.startswith(_ANSWER_SYNTAX) and buffer.endswith(_LINE_BREAK):
							completed = int(n(buffer[7:-1])) #TODO regex.
							buffer = b("")
						completed -= 1
					except socket.timeout:
						raise NoResponse(command)
						if self.debug:
							print("Timed out, retry.")
						continue  # just ignore and retry. Is used to be able to quit.
					except KeyboardInterrupt as error:
						print("Exception while reading the Answer for \"%s\". Got so far: >%s< of %i\n" % (n(command),n(buffer),completed))  # TODO remove me
						s.close()
						raise
					except Exception as error:
						print("Exception while reading the Answer for \"%s\". Got so far: >%s<\n" % (n(command),n(buffer))) #TODO remove me
						s.close()
						raise
						#raise error
				# end while completed != 0
				if s:
					s.close()
				return u(buffer)
		# end block
		if s:
			s.close()


class NoResponse(Exception):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)