__author__ = 'luckydonald'
import argumenttypes as args

class Send(object):
	def __init__(self):
		pass

	functions = {
		"get_contact_list": [],
		"get_dialog_list": [],
		"rename_chat": [args.chat, args.string],
		"send_msg": [args.peer, args.string],
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
		self._do_command(function_name(*arguments));
		pass

	def __getattr__(self, attr):
		if attr in self.functions:
			return self.Command(attr, self)
		else:
			return object.__getattribute__(self, attr)

	def _do_command(self, function_sting, *args):
		arg_string = " ".join([str(x) for x in args])
		request = " ".join([function_sting, arg_string])
		print("Command: %s" %request)
		return request

	class Command:
		def __init__(self, name, tg):
			self.name = name
			self.tg = tg

		def __call__(self, *args):
			return self.tg._do_command(self.name, *args)


if __name__ == '__main__':
	x = Send()
	print(x)
	res = x.mark_read("luckydonald")
	print(res)