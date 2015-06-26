class PytgObjectOrigin(object):
	def __init__(self, type):
		super(PytgObjectOrigin).__init__()
		self.type = type

	def __repr__(self, *args, **kwargs):
		return "PytgObjectOrigin({type})".format(type=self.type)
TGL = PytgObjectOrigin("tgl")
SOCKET = PytgObjectOrigin("socket")
PytgObjectOrigin.TGL = TGL
PytgObjectOrigin.SOCKET = SOCKET

class PytgObject(object):
	"""
	Parent class of all Types.
	Contain information from where the object is, either socket or tgl.
	"""
	def __init__(self, origin):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin
		"""
		super(PytgObject).__init__()
		if origin is None:
			raise TypeError("Parameter origin is None")
		if not isinstance(origin, PytgObjectOrigin):
			raise TypeError("parameter origin is not type PytgObjectOrigin")
		self.origin = origin

	def __repr__(self):
		return "{type}({values})".format(type=self.__class__.__name__, values=", ".join(["{key}={value}".format(key=k, value=repr(v)) for k,v in self.__dict__.items()]))

	def __contains__(self, item):
		return item in self.__dict__

class Forward(PytgObject):
	"""
	Contains infos about from who an when this message was forwarded.
	See __init__ for variables.
	"""

	def __init__(self, origin, date, sender):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param date: Time the original message of this forward was send in the first place.
		:type  date: datetime.datetime

		:param sender: The user who send that massage in the first place.
		:type  sender: User
		"""
		super(Forward, self).__init__(origin)
		self.date = date
		self.sender = sender
	# end def __init__
# end of class Forward


class Reply(PytgObject):
	"""
	Contains infos about from who an when this message was forwarded.
	See __init__ for variables.
	"""

	def __init__(self, origin, id, message=None):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param id: Message id.
		:type  id: int

		:param message: The original Message, if cached automatically.
		:type  message: Message | None
		"""
		super(Reply, self).__init__(origin)
		if not isinstance(id, int):
			raise TypeError("Parameter id is not type int")
		if message is not None and not isinstance(message, Message):
			raise TypeError("Parameter message is not type Message")
		self.id = id
		self.message = message
	# end def __init__
# end of class Forward


class UserStatus(PytgObject):
	"""
	A status of a User.
	See __init__ for variables.
	"""

	def __init__(self, origin, online, when):
		"""
		Has a boolean if online, and when it was online last.

		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param online: If the User is currently online.
		:type  online: bool

		:param when: When the User was the last time online.
		:type  when: datetime.datetime

		"""
		super(UserStatus, self).__init__(origin)
		self.online = online
		self.when = when
		pass


class Media(PytgObject):
	def __init__(self, origin, message_id, type_str):
		"""
		Superclass for all Media types. Very sporadic, as they don't have much in common.

		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param message_id: Message Id this is related to.
		:type  message_id: int
		"""
		super(Media, self).__init__(origin)
		if not isinstance(message_id, int):
			raise TypeError("Parameter message_id is not type int")
		if not isinstance(type_str, str):
			raise TypeError("Parameter type_str is not type str")
		self.message_id = message_id
		self.type_str = type_str
	# end def __init__
# end class Media


class Message(PytgObject):
	"""
	A Message someone sent.
	See __init__ for variables.
	"""
	def __init__(self, origin, id, date, sender, receiver, own, mention, unread, service, flags, queued_events, fwd=None, reply=None, media=None, text=None):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

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

		:param queued_events: The currently queued messages. Set to 0 if there is no such information.
		:type  queued_events: int

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
		super(Message, self).__init__(origin)
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
		self.queued_events = queued_events



class Peer(PytgObject):
	"""
	A Peer. User and Chat objects have this class as superclass.
	"""
	USER = "user"
	CHAT = "chat"
	ENCRYPTED = "encr"

	def __init__(self, origin, id, type_str, name):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param id: The identifier number of the peer (user/group)
		:type  id: int

		:param type_str: The type.
		:type  type_str: str

		:param name: User or chat name.
		:type  name: str

		:return:
		"""
		super(Peer, self).__init__(origin)
		self.id = id				# tgl.Peer.id
		self.type_str = type_str	# tgl.Peer.type_name
		self.name = name			# tgl.Peer.name


class User(Peer):
	def __init__(self, origin, id, name, first_name, last_name, phone, username, status):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

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
		super(User, self).__init__(origin, id, Peer.USER, name)
		self.first_name = first_name	# tgl.Peer.first_name
		self.last_name = last_name		# tgl.Peer.last_name
		self.phone = phone				# tgl.Peer.phone
		self.username = username		# tgl.Peer.username
		self.status = status			# tgl.Peer.user_status


class Chat(Peer):
	def __init__(self, origin, id, name, user_list, user_count, admin_id):
		"""
		A group chat. Is subclass of Peer.

		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param user_list: A list of user ids in that chat. List can be empty if not cached yet. Use chat_info() first.
		:type  user_list: list of int

		:param user_count: How many users are in the chat, to check if the user_list array was loaded completely.
		:type  user_count: int

		:param admin_id: Id of user who is admin in that chat.
		:type  admin_id: int

		"""
		super(Chat, self).__init__(origin, id, Peer.CHAT, name)
		if user_list is not None and not isinstance(user_list, list):
			raise TypeError("Parameter user_list is not type list, but type {type}".format(type=type(user_list)))
		if not isinstance(admin_id, int):
			raise TypeError("Parameter admin_id is not type int, but type {type}".format(type=type(admin_id)))
		if not isinstance(user_count, int):
			raise TypeError("Parameter user_count is not type int, but type {type}".format(type=type(user_count)))
		self.user_list = user_list	# tgl.Peer.users
		self.admin_id = admin_id	# tgl.Peer. ???? # does not exist yet.
		self.user_count = user_count

	def __le__(self, *args, **kwargs):
		if self.user_list is None:
			return self.user_count
		else:
			return max(len(self.user_list), self.user_count)


class Location(Media):
	"""
	This is a location Media. (aka. "geo")
	"""

	def __init__(self, origin, message_id, latitude, longitude):
		"""
		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param message_id: Message Id this is related to.
		:type  message_id: int

		:param latitude: the latitude of the location.
		:type  latitude: float

		:param longitude: the longitude of the location.
		:type  longitude: float
		"""
		super(Location, self).__init__(origin, message_id, "geo")
		if not isinstance(latitude, (float, int)):
			raise TypeError("Parameter latitude is not type (float, int)")
		if not isinstance(longitude, (int, float)):
			raise TypeError("Parameter longitude is not type (int, float)")
		self.latitude = float(latitude)
		self.longitude = float(longitude)

class Photo(Media):
	def __init__(self, origin, message_id, caption):
		"""
		A photo. Compressed Image.

		:param origin: Where the message is from. Either TGL or SOCKET.
		:type  origin: PytgObjectOrigin

		:param message_id: Message Id this is related to.
		:type  message_id: int

		:param caption: If there is a caption with the image.
		:type  caption: str | None
		"""
		super(Photo, self).__init__(origin, message_id, "photo")
		if caption is not None and not isinstance(caption, str):
			raise TypeError("Parameter caption is not type str")
		self.caption = caption

class Document(Media):
	def __init__(self, origin, message_id):
		super(Document, self).__init__(origin, message_id, "document")