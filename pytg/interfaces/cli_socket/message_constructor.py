# -*- coding: utf-8 -*-

__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)



from ...types import Message, Reply, UserStatus, Peer, User, Chat, Forward, Location, Photo
from ...types import SOCKET as TYPE_SOCKET
from ..access import MessageConstructorSuperclass


#from pytg.types import Message, Reply, UserStatus, Peer, User, Chat, Forward, Location, Photo
#from pytg.types import SOCKET as TYPE_SOCKET

class MessageConstructor(MessageConstructorSuperclass):
	
	def new_peer(self, peer):
		if peer["type"] == Peer.USER:
			phone = peer["phone"] if "phone" in peer else None
			return User(TYPE_SOCKET, peer["id"], peer["print_name"], peer["first_name"], peer["last_name"], phone, peer["username"], None)
		elif peer["type"] == Peer.CHAT:
			users_list = []
			logger.debug("WARNING: Chat.user_list not supported in cli_socket.")
			return Chat(TYPE_SOCKET, peer["id"], peer["print_name"], users_list, peer["members_num"], peer["admin"]["id"])
	
	
	def new_fwd(self, fwd_date, fwd_src):
		return Forward(TYPE_SOCKET, fwd_date, fwd_src)
	
	
	def new_media(self, media, message_id):
		if media is None:
			return None
		assert isinstance(media, dict)
		assert "type" in media
		if media["type"] == "geo":	# {'latitude': 53.779889, 'type': 'geo', 'longitude': -1.755313}
			assert "latitude" in media
			assert "longitude" in media
			return Location(TYPE_SOCKET, message_id, media["latitude"], media["longitude"])
		elif media["type"] == "photo":
			assert "caption" in media
			return Photo(TYPE_SOCKET, message_id, media["caption"])
			pass
		elif media["type"] == "":
			pass
		elif media["type"] == "":
			pass
		elif media["type"] == "":
			pass
		elif media["type"] == "":
			pass
		else:
			logging.warning("Unhandled media type: {type}".format(type=media["type"]))
		if media is None:
			return None
	
	
	def new_reply(self, id, message):
		if id is None:
			return None
		return Reply(TYPE_SOCKET, id, message)
	
	def new_event(self, msg):
		assert "event" in msg
		if msg["event"] == "online-status":
			logger.warn("online-status event not implemented")
		elif msg["event"] == "message":
			return self.new_message(msg)
	
	def new_message(self, msg):
		if msg == None:
			logging.debug("Message was None.")
			return None
		assert "id" in msg
		assert "date" in msg
		assert "from" in msg
		assert "to" in msg
		assert "out" in msg
		assert "unread" in msg
		mention = msg["mention"] if "mention" in msg else None
		reply = self.new_reply(msg["reply_id"], None) if "reply_id" in msg else None
		forward = self.new_fwd(msg["fwd_date"], msg["fwd_from"]) if "fwd_date" in msg and "fwd_from" in msg else None
		text = msg["text"] if "text" in msg else None
		media = self.new_media(msg["media"], msg["id"]) if "media" in msg else None
		return Message(TYPE_SOCKET, msg["id"], msg["date"], self.new_peer(msg["from"]), self.new_peer(msg["to"]), msg["out"], mention, msg["unread"],
					   msg["service"], msg["flags"], fwd=forward, reply=reply,
					   media=media, text=text
		)
	# end def

	def new_userstatus(self, user_status):
		"""
		Transforms a dict with status informations into a UserStatus object.
	
		:param user_status: A dict like {'when': datetime.datetime(2015, 6, 12, 21, 50, 52), 'online': True}
		:type  user_status: dict
	
		:return: A UserStatus object.
		:rtype: UserStatus
		"""
		assert isinstance(user_status, dict)
		assert "when" in user_status
		assert "online" in user_status
		return UserStatus(TYPE_SOCKET, user_status["online"], user_status["when"])
	

#msg = {'to': {'type': 'chat', 'title': 'Bot Dev Test Group', 'members_num': 14, 'print_name': 'Bot_Dev_Test_Group', 'id': 19269926, 'admin': {'print_name': 'user#0', 'id': 0, 'type': 'user'}, 'flags': 256}, 'out': False, 'from': {'type': 'user', 'first_name': 'otouto', 'print_name': 'otouto', 'id': 66603334, 'username': 'otouto', 'last_name': '', 'flags': 256}, 'media': {'type': 'photo', 'caption': ''}, 'date': 1435254027, 'event': 'message', 'id': 42124, 'service': False, 'unread': True, 'flags': 257}
#new_message(msg)
