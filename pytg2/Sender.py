__author__ = 'luckydonald'
from . import argumenttypes as args
from .utils import suppress_context, escape
from .encoding import to_native as n
from .encoding import to_unicode as u
from .encoding import text_type
import socket # connect to telegram cli.
from errno import ECONNREFUSED
from socket import error as socket_error
import threading

SOCKET_SIZE = 1 << 25
FUNC_CMD  = 0
FUNC_ARGS = 1
class Sender(object):
	def __init__(self, host, port):
		self.host = host
		self.port_out = port
		self.__all__ = [x for x in self.functions]

	_socked_used = threading.Semaphore(1)

	functions = {
		"get_contact_list":		["contact_list",		[]],
		"get_dialog_list": 		["dialog_list", 		[]],
		"rename_chat": 			["rename_chat", 		[args.chat, args.unicode_string]],
		"send_msg": 			["msg", 				[args.peer, args.unicode_string]],
		"send_typing": 			["send_typing", 		[args.peer, args.nonnegative_number]],
		"send_typing_abort": 	["send_typing_abort", 	[args.peer]],
		"send_photo": 			["send_photo", 			[args.peer, args.unicode_string]],
		"send_video": 			["send_video", 			[args.peer, args.unicode_string]],
		"send_audio": 			["send_audio", 			[args.peer, args.unicode_string]],
		"send_document": 		["send_document", 		[args.peer, args.unicode_string]],
		"send_file": 			["send_file", 			[args.peer, args.unicode_string]],
		"send_text": 			["send_text", 			[args.peer, args.unicode_string]],
		"chat_set_photo": 		["chat_set_photo", 		[args.chat, args.unicode_string]],
		"load_photo": 			["load_photo", 			[args.msg_id]],
		"load_video": 			["load_video", 			[args.msg_id]],
		"load_video_thumb": 	["load_video_thumb", 	[args.msg_id]],
		"load_audio": 			["load_audio", 			[args.msg_id]],
		"load_document": 		["load_document", 		[args.msg_id]],
		"load_document_thumb": 	["load_document_thumb", [args.msg_id]],
		"fwd_msg": 				["fwd",		 			[args.peer, args.msg_id]],
		"fwd_media": 			["fwd_media", 			[args.peer, args.msg_id]],
		"chat_info": 			["chat_info", 			[args.chat]],
		"user_info": 			["user_info", 			[args.user]],
		"get_history": 			["history", 			[args.peer, args.nonnegative_number]],
		"chat_add_user": 		["chat_add_user", 		[args.chat, args.user]],
		"chat_del_user": 		["chat_del_user", 		[args.chat, args.user]],
		"add_contact": 			["add_contact", 		[args.unicode_string, args.unicode_string, args.unicode_string]],
		"del_contact": 			["del_contact", 		[args.user]],
		"rename_contact": 		["rename_contact", 		[args.unicode_string, args.unicode_string, args.unicode_string]],
		"msg_search": 			["msg_search", 			[args.peer, args.unicode_string]],
		"msg_global_search": 	["msg_global_search", 	[args.unicode_string]],
		"mark_read": 			["mark_read", 			[args.peer]],
		"set_profile_photo": 	["set_profile_photo", 	[args.unicode_string]],
		"set_profile_name": 	["set_profile_name", 	[args.unicode_string]],
		"create_secret_chat": 	["create_secret_chat", 	[args.user]],
		"create_group_chat": 	["create_group_chat", 	[args.user, args.unicode_string]],
		"delete_msg": 			["delete_msg", 			[args.msg_id]],
		"restore_msg": 			["restore_msg", 		[args.positive_number]],
		"accept_secret_chat": 	["accept_secret_chat", 	[args.secret_chat]],
		"send_contact": 		["send_contact", 		[args.peer, args.unicode_string, args.unicode_string, args.unicode_string]],
		"status_online": 		["status_online", 		[]],
		"status_offline": 		["status_offline", 		[]],
		"send_location": 		["send_location", 		[args.peer, args.double, args.double]],
		"ext_function": 		["", 					[args.unicode_string]]
	}
	# \{"(.*)",\ .*,\ \{\ (.*)\ \}\}, >> "$1": ["$1", [$2]],

	def execute_function(self, function_name, *arguments):
		arguments_types = self.functions[function_name][FUNC_ARGS]
		command_name = self.functions[function_name][FUNC_CMD]
		if (len(arguments) != len(arguments_types)):
			raise ValueError("Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(function_name=function_name, expected_number=len(arguments_types), given_number=len(arguments)))
		i = 0
		new_args = []
		for arg in arguments:
			func_type = arguments_types[i]
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
		if attr in self.functions:
			print("newly: %s" % attr)
			command = self.Command(attr, self)
			setattr(self, attr, command)
			return command
		else:
			return object.__getattribute__(self, attr)

	def _do_command(self, function_sting, *argmts):
		arg_string = " ".join([str(x) for x in argmts])
		request = "".join([function_sting, " ", arg_string, "\n"])
		result = self._do_send(request)
		return result

	class Command:
		def __init__(self, name, sender_instance):
			self.name = name
			self.sender_instance = sender_instance

		def __call__(self, *args):
			return self.sender_instance.execute_function(self.name, *args)

	def _do_send(self, command):
		with self._socked_used.acquire():
		self._socked_used.acquire()
		print("sending {command}".format(command=command))
		s = socket.socket()
		try:
			s.connect((self.host,self.port_out))
		except socket_error as error:
			s.close()
			if error.errno != ECONNREFUSED:
				raise suppress_context(socket_error)  # Not the error we are looking for, re-raise
			print("Connection to Receiver CLI refused.\nMaybe not running?")
			self._socked_used.release()
			return
		print("Connected.")
		try:
			s.send(command.encode("utf-8")) #TODO be py2/3 compatible
		except socket_error as error:
			s.close()
			self._socked_used.release()
			raise suppress_context(socket_error)
		print("Sended.")
		completed = -1 # -1 = answer size yet unknown, >0 = got remaining answer size
		buffer = u("")
		while(completed != 0):
			try:
				s.settimeout(10) # in seconds.
				answer = u(s.recv(1))
				buffer += answer
				if completed <= -1 and buffer.startswith(u("ANSWER ")) and  buffer.endswith(u("\n")):
					completed = int(n(buffer[7:-1])) #TODO regex.
					buffer = u("")
				completed -= 1
			except socket_error as error:
				print("Failed")
				s.close()
				self._socked_used.release()
				raise suppress_context(error)
		s.close()
		self._socked_used.release()
		return buffer





