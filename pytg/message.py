__author__ = 'luckydonald'

try:
	from enum import Enum
except ImportError:
	from __builtin__ import object as Enum #wow this is hacky!



arg = {'type': 'message', 'msgid': m.group('msgid'), 'timestamp': m.group('timestamp'),
				       'message': m.group('message'), 'media': None, 'peer': 'group' if (m.group('chatid')) else 'user',
				       'group': m.group('chat'), 'groupid': m.group('chatid')}

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
		self.reply_to =

class PeerType(object):
    def __str__(self):
        return "unknown chat type"
    def __get__(self,*args,**kwargs):
        return self()

class Group(PeerType):
    def __str__(self):
        return "group chat"

class User(PeerType):
    def __str__(self):
        return "user chat"

class Secret(PeerType):
    def to_string(self):
        return "secret user chat"
    __str__ = to_string

class Peer(object):
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
        if not issubclass(type, PeerType):
            raise TypeError("Type need to be a Peer.PeerType")
        #end if
        if type == Group:
            self.cmd = "chat#" + id
        elif type == User:
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

test = Peer(Peer.GROUP, "1145512", "Ponies!!!")

class toObject(dict):
    # stout("processing" + str(object))
    def __init__(self, d,  **kwargs):
        super(toObject, self).__init__(d,  **kwargs)
        if not isinstance(d, dict):
            raise TypeError("is no dict.")
        self._dict = d
        for a, b in d.items():
            if isinstance(b, (list, tuple)): # add all list elements
                setattr(self, a, [toObject(x) if isinstance(x, (dict,list,tuple)) else x for x in b])
            elif isinstance(b, dict):# add list recursivly
                setattr(self, a, toObject(b))
            elif str(a).isdigit(): #add single numeric-element
                setattr(self, a, str(b))
                setattr(self, "_" + str(a), b) #to access  a = {'1':'foo'}  with toObject(a)._1
            else: #add single element
                setattr(self, a, b)
