

#{"id": 40771,
# "fwd_date":
#	 1434125526, "event": "message", "flags": 257, "fwd_from": {"id": 10717954, "last_name": "", "type": "user", "username": "luckydonald", "first_name": "luckydonald", "print_name": "luckydonald", "flags": 257, "phone": "4917631763460"}, "out": false, "date": 1434125539, "to": {"id": 77994709, "last_name": "", "type": "user", "username": "derpybot", "first_name": "Derpybot", "print_name": "Derpybot", "flags": 264, "phone": "4915902296258"}, "service": false, "from": {"id": 10717954, "last_name": "", "type": "user", "username": "luckydonald", "first_name": "luckydonald", "print_name": "luckydonald", "flags": 257, "phone": "4917631763460"}, "unread": true, "text": "!sad"}

class Forward(object):
	"""
	Contains infos about from who an when this message was forwarded.
	See __init__ for variables.
	"""

	def __init__(self, date, sender):
		"""
		:param date: Time the original message of this forward was send in the first place.
		:type  date: datetime.datetime

		:param sender: The user who send that massage in the first place.
		:type  sender: User
		"""
		self.date = date
		self.sender = sender
	# end def __init__
# end of class Forward

class UserStatus(object):
	"""
	A status of a User.
	See __init__ for variables.
	"""

	def __init__(self, online, when):
		"""
		Has a boolean if online, and when it was online last.

		:param online: If the User is currently online.
		:type  online: bool

		:param when: When the User was the last time online.
		:type  when: datetime.datetime

		"""
		self.online = online
		self.when = when
		pass


class Media(object):
	def __init__(self, type_str):
		"""
		Superclass for all Media types. Very sporadic, as they don't have much in common.
		"""
		self.type_str = type_str
	# end def __init__
# end class Media


class Message(object):
	"""
	A Message someone sent.
	See __init__ for variables.
	"""
	def __init__(self, id, date, sender, receiver, own, mention, unread, service, flags, fwd=None, reply=None, media=None, text=None):
		"""
		:param id: The message id.
		:type  id: int

		:param date: When the message was received by the cli.
		:type  date: datetime.datetime

		:param sender: Who send the message. This Peer type is always type User.
		:type  sender: User

		:param receiver: Who the message was sent to. This Peer can be either a User or a (group) Chat.
		:type  receiver: User | Chat

		:param own: If a message is send from our account. (cli or somewhere else)
		:type  own: bool

		:param mention: If we got mentioned in the message. (If the message included our @username.)
		:type  mention: bool

		:param unread: If the message was already read.
		:type  unread: bool

		:param service: ??? If it is a service. Whatever that actually means...
		:type  service: bool

		:param flags: Attributes used internally in the cli. You probably want to ignore that.
		:type  flags: int

		:param fwd: Contains infos about from who an when this message was forwarded.
		:type  fwd: Forward | None

		:param reply: The original message this message was a reply to.
		:type  reply: Message | None

		:param media: The media of the message. Can be None.
		:type  media: Media | None

		:param text: The text of the message, if it is a text message.
		:type  text: str | None

		:return:
		"""
		self.id = id				# tgl.Msg.id
		self.date = date			# tgl.Msg.date
		self.sender = sender 		# tgl.Msg.src
		self.receiver = receiver 	# tgl.Msg.dest
		self.fwd = fwd				# tgl.Msg.fwd_date & Msg.fwd_src
		self.reply = reply			# tgl.Msg.reply (& Msg.reply_id)
		self.own = own				# tgl.Msg.out
		self.mention = mention		# tgl.Msg.mention
		self.service = service		# tgl.Msg.service
		self.media = media			# tgl.Msg.media
		self.text = text			# tgl.Msg.text
		self.unread = unread		# tgl.Msg.unread
		self.flags = flags			# tgl.Msg.flags


class Peer(object):
	"""
	A Peer. User and Chat objects have this class as superclass.
	"""
	USER = "user"
	CHAT = "chat"
	ENCRYPTED = "encr"

	def __init__(self, id, type_str, name):
		"""
		:param id: The identifier number of the peer (user/group)
		:type  id: int

		:param type_str: The type.
		:type  type_str: str

		:param name: User or chat name.
		:type  name: str

		:return:
		"""
		self.id = id				# tgl.Peer.id
		self.type_str = type_str	# tgl.Peer.type_name
		self.name = name			# tgl.Peer.name


class User(Peer):
	def __init__(self, id, name, first_name, last_name, phone, username, status):
		"""

		:param id: The identifier number of the peer
		:type  id: int

		:param name: The displayed name.
		:type  name: str

		:param first_name: First name of the users full name
		:type  first_name: str

		:param last_name: Last name of the users full name
		:type  last_name: str

		:param phone: Phone number, without leading '+' sign
		:type  phone: str

		:param username: the @username, without the '@'-sign
		:type  username: str

		:param status: More informations about the user status, currently in a dict.
		:type  status: UserStatus
		"""
		super().__init__(id, Peer.USER, name)
		self.first_name = first_name	# tgl.Peer.first_name
		self.last_name = last_name		# tgl.Peer.last_name
		self.phone = phone				# tgl.Peer.phone
		self.username = username		# tgl.Peer.username
		self.status = status			# tgl.Peer.user_status


class Chat(Peer):
	def __init__(self, id, name, users, admin):
		"""
		A group chat. Is subclass of Peer.

		:param users: A list of user ids in that chat. List can be empty if not cached yet. Use chat_info() first.
		:type  users: dict of int

		:param admin: Who is admin in that chat.
		:type  admin: User

		"""
		super().__init__(id, Peer.CHAT, name)
		self.users = users		# tgl.Peer.user_list
		self.admin = admin		# tgl.Peer. ???? # does not exist yet.


class Location(Media):
	"""
	This is a location Media. (aka. "geo")
	"""

	def __init__(self, latitude, longitude):
		"""
		:param latitude: the latitude of the location.
		:type  latitude: float

		:param longitude: the longitude of the location.
		:type  longitude: float
		"""
		super().__init__("geo")
		self.latitude = latitude
		self.longitude = longitude