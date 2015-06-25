# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)



from ..types import Message, Reply, UserStatus, Peer, User, Chat, Forward, Location, Photo
from ..types import SOCKET as TYPE_SOCKET


def new_peer(peer):
	if peer["type"] == Peer.USER:
		phone = peer["phone"] if "phone" in peer else None
		return User(TYPE_SOCKET, peer["id"], peer["print_name"], peer["first_name"], peer["last_name"], phone, peer["username"], None)
	elif peer["type"] == Peer.CHAT:
		return Chat(TYPE_SOCKET, peer["id"], peer["print_name"], None, peer["admin_id"]["id"])


def new_fwd(fwd_date, fwd_src):
	return Forward(TYPE_SOCKET, fwd_date, fwd_src)


def new_media(media, message_id):
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


def new_reply(id, message):
	if id is None:
		return None
	return Reply(TYPE_SOCKET, id, message)


def new_message(msg):
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
	reply = new_reply(msg["reply_id"], None) if "reply_id" in msg else None
	forward = new_fwd(msg["fwd_date"], msg["fwd_from"]) if "fwd_date" in msg and "fwd_from" in msg else None
	text = msg["text"] if "text" in msg else None
	media = new_media(msg["media"], msg["id"]) if "media" in msg else None
	return Message(TYPE_SOCKET, msg["id"], msg["date"], new_peer(msg["from"]), new_peer(msg["to"]), msg["out"], mention, msg["unread"],
				   msg["service"], msg["flags"], fwd=forward, reply=reply,
				   media=media, text=text)




def new_userstatus(user_status):
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



