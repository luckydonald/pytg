from pytg2 import suppress_context

__author__ = 'luckydonald'
import argumenttypes as args
import socket # connect to telegram cli.
from errno import ECONNREFUSED
from socket import error as socket_error

SOCKET_SIZE = 1 << 25

class Sender(object):
	def __init__(self, host, port):
		self.host = host
		self.port_out = port
		self.__all__ = [x for x in self.functions]


	functions = {
		"get_contact_list": [],
		"dialog_list": [], #get_dialog_list
		"rename_chat": [args.chat, args.string],
		"msg": [args.peer, args.string],
		"send_typing": [args.peer, args.nonnegative_number],
		"send_typing_abort": [args.peer],
		"send_photo": [args.peer, args.string],
		"send_video": [args.peer, args.string],
		"send_audio": [args.peer, args.string],
		"send_document": [args.peer, args.string],
		"send_file": [args.peer, args.string],
		"send_text": [args.peer, args.string],
		"chat_set_photo": [args.chat, args.string],
		"load_photo": [args.msg_id],
		"load_video": [args.msg_id],
		"load_video_thumb": [args.msg_id],
		"load_audio": [args.msg_id],
		"load_document": [args.msg_id],
		"load_document_thumb": [args.msg_id],
		"fwd_msg": [args.peer, args.msg_id],
		"fwd_media": [args.peer, args.msg_id],
		"chat_info": [args.chat],
		"user_info": [args.user],
		"get_history": [args.peer, args.nonnegative_number],
		"chat_add_user": [args.chat, args.user],
		"chat_del_user": [args.chat, args.user],
		"add_contact": [args.string, args.string, args.string],
		"del_contact": [args.user],
		"rename_contact": [args.string, args.string, args.string],
		"msg_search": [args.peer, args.string],
		"msg_global_search": [args.string],
		"mark_read": [args.peer],
		"set_profile_photo": [args.string],
		"set_profile_name": [args.string],
		"create_secret_chat": [args.user],
		"create_group_chat": [args.user, args.string],
		"delete_msg": [args.msg_id],
		"restore_msg": [args.positive_number],
		"accept_secret_chat": [args.secret_chat],
		"send_contact": [args.peer, args.string, args.string, args.string],
		"status_online": [],
		"status_offline": [],
		"send_location": [args.peer, args.double, args.double],
		"ext_function": [args.string]
	}
	# \{"(.*)",\ .*,\ \{\ (.*)\ \}\}, >> "$1": [$2],

	def execute_function(self, function_name, *arguments):
		function = self.functions[function_name]
		i = 0
		if (len(arguments) != len(function)):
			raise ValueError("Error in function {function_name}: {expected_number} paramters expected, but {given_number} were given.".format(function_name=function_name, expected_number=len(function), given_number=len(arguments)))
		for arg in arguments:
			func_type = function[i]
			if not func_type(arg):
				raise ValueError("Error in function {function_name}: parameter {number} is not type {type}.".format(function_name=function_name, number=i, type=func_type.__name__))
			i += 1
		# end for
		return self._do_command(function_name,*arguments);

	def __getattr__(self, attr):
		if attr in self.functions:
			return self.Command(attr, self)
		else:
			return object.__getattribute__(self, attr)

	def _do_command(self, function_sting, *args):
		arg_string = " ".join([str(x) for x in args])
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
		print("sending {command}".format(command=command))
		s = socket.socket()
		try:
			s.connect((self.host,self.port_out))
		except socket_error as error:
			s.close()
			if error.errno != ECONNREFUSED:
				raise suppress_context(socket_error)  # Not the error we are looking for, re-raise
			print("Connection to Telegram CLI refused.\nMaybe not running?")
			return
		print("Connected.")
		try:
			s.send(command.encode("utf-8")) #TODO be py2/3 compatible
		except socket_error as error:
			s.close()
			raise suppress_context(socket_error)
		print("Sended.")
		completed = -1 # -1 = answer size yet unknown, >0 = got remaining answer size
		buffer = ""
		while(completed != 0):
			try:
				s.settimeout(10) # in seconds.
				answer = s.recv(1)
				buffer += answer
				if completed <= -1 and buffer.startswith("ANSWER ") and  buffer.endswith("\n"):
					completed = int(buffer[7:-1]) #TODO regex.
					buffer = ""
				completed -= 1
			except socket_error as error:
				print("Failed")
				s.close()
				raise suppress_context(socket_error)
		s.close()
		return buffer

if __name__ == '__main__':
#def ____():
	"""
	Test only.
	>>> x = Sender("127.0.0.1", 1337)
	>>> x.msg("luckydonald",5)
	SUCCESS
	>>> x.send_typing("luckydonald",9)
	SUCCESS
	>>> x.send_typing("luckydonald",900)
	FAIL

	"""
	# Test.

	x = Sender("127.0.0.1", 1337)  # 9034
	#res = x.msg("luckydonald",5)
	# res = x.mark_read("luckydonald")
	#print("Got: %s" % res)
	res = x.dialog_list()
	print("Got: >%s<" % res)



