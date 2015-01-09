__author__ = 'luckydonald'


import sys # py version check.


class Printable(type):
	def __repr__(self):
		return self.__str__().join(["'", "'"])
	def __str__(self):
			return self.__str__()
class Peer(object):

	if sys.version < '3': # python 2.7
		class PeerType(object):
			__metaclass__ = Printable
			@classmethod
			def __str__(cls):
				return "unknown chat type"
			prefix = None
		class Group(PeerType):
			__metaclass__ = Printable
			@classmethod
			def __str__(self):
				return "group chat"
			prefix = "chat"
		class User(PeerType):
			__metaclass__ = Printable
			@classmethod
			def __str__(self):
				return "user chat"
			prefix = "chat"
		class Secret(PeerType):
			__metaclass__ = Printable
			def to_string(self):
				return "secret user chat"
			__str__ = to_string
	else: # python 3
		class PeerType(object, metaclass=Printable):
			@classmethod
			def __str__(cls):
				return "unknown chat type"
			prefix = None
		class Group(PeerType, metaclass=Printable):
			@classmethod
			def __str__(self):
				return "group chat"
			prefix = "chat"
			type = "group"
		class User(PeerType, metaclass=Printable):
			@classmethod
			def __str__(self):
				return "user chat"
			prefix = "user"
			type = "user"
		class Secret(PeerType, metaclass=Printable):
			def to_string(self):
				return "secret user chat"
			__str__ = to_string

	GROUP = Group
	USER = User
	SECRET = Secret
	#
	# now the object:
	type = None
	cmd = None
	name = None
	id = None
	namecmd = None
	#
	def __init__(self, type, id, name):
		if not issubclass(type, Peer.PeerType):
			raise TypeError("Type need to be a Peer.PeerType")
		#end if
		if type == Peer.Group:
			self.cmd = "chat#" + id
			# self.type =
		elif type == Peer.User:
			self.cmd = "user#" + id
		else:
			raise TypeError("Peer type {0} unsupported {0}.".format(type,Peer.GROUP))
		#end if
		self.type = type
		try:
			self.id = int(id)
		except Exception:
			raise
		#end try
		self.name = name
		self.namecmd = name.replace(" ","_").replace("#","@")
	def __str__(self):
		return "#".join([self.type.prefix,self.name,str(self.id)])
	def __repr__(self):
		return self.__str__().join(["'","'"])


# test = Peer(Peer.GROUP, "1145512", "Ponies!!!")

#arg = {'type': 'message', 'msgid': m.group('msgid'), 'timestamp': m.group('timestamp'),
#				       'message': m.group('message'), 'media': None, 'peer': 'group' if (m.group('chatid')) else 'user',
#				       'group': m.group('chat'), 'groupid': m.group('chatid')}

#arg = {'media': None, 'ownmsg': False, 'groupid': '1145512', 'peer': 'group', 'message': 'und chrysalis ist immer noch unter den Ponies in canterlot', 'user': '\uf8ff', 'timestamp': '17:34', 'type': 'message', 'usercmd': '\uf8ff', 'group': 'Ponies!!!', 'msgid': '83334', 'groupcmd': 'Ponies!!!', 'userid': '30445578'}
#arg["userpeer"] = Peer(Peer.GROUP, "1145512", "Ponies!!!")




""" # the rest is unfinished...


class Message(object):
	is_own_msg = True
	message = None
	user_peer = None
	msgid = 0
	timestamp = ''
	def __init__(self, message, timestamp, is_own_msg, user_peer):
		if not isinstance(user_peer, Peer):
			raise TypeError("peer need to be of type Peer")
		self.message = message
		self.timestamp = timestamp
		self.user_peer = user_peer
		self.is_own_msg = is_own_msg
		self.reply_to = user_peer

#	{'media': None, 'ownmsg': False, 'groupid': '1145512', 'peer': 'group', 'message': 'und chrysalis ist immer noch unter den Ponies in canterlot', 'user': '\uf8ff', 'timestamp': '17:34', 'type': 'message', 'usercmd': '\uf8ff', 'group': 'Ponies!!!', 'msgid': '83334', 'groupcmd': 'Ponies!!!', 'userid': '30445578'}
class ChatMessage(Message):
	def __init__(self, message, timestamp, is_own_msg, user_peer):
		super(ChatMessage, self).__init__(message, timestamp, is_own_msg, user_peer)


"""
