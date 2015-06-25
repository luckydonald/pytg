# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging

logger = logging.getLogger(__name__)
import tgl
import sys

sys.path.append("/path/to/pycharm_debugger/pycharm-debug-py3k.egg")
sys.path.append("/path/to/pytg")
try:
	import pydevd
	pydevd.settrace('localhost', port=4457, stdoutToServer=True, stderrToServer=True, suspend=False)
except ImportError:
	logger.debug("Failed to import debugger.")

logging.basicConfig(level=logging.DEBUG)

from ..types import Message, Forward, User, Chat, Peer, UserStatus, Location, TGL, Reply


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
	return UserStatus(TGL, user_status["online"], user_status["when"])


def new_peer(peer):
	assert isinstance(peer, tgl.Peer)
	if peer.type_name == Peer.USER:
		return User(TGL, peer.id, peer.name, peer.first_name, peer.last_name, peer.phone, peer.username, new_userstatus(peer.user_status))
	elif peer.type_name == Peer.CHAT:
		return Chat(TGL, peer.id, peer.name, peer.user_list, 0)


def new_reply(id, message):
	if id is None:
		return None
	return Reply(TGL, id, message)


def new_message(msg):
	if msg == None:
		logging.debug("Message was None.")
		return None
	assert isinstance(msg, tgl.Msg)
	return Message(TGL, msg.id, msg.date, new_peer(msg.src), new_peer(msg.dest), msg.out, msg.mention, msg.unread,
				   msg.service, msg.flags, fwd=new_fwd(msg.fwd_date, msg.fwd_src), reply=new_reply(msg.reply_id,msg.reply),
				   media=new_media(msg.id, msg.media), text=msg.text)


def new_fwd(fwd_date, fwd_src):
	return Forward(TGL, fwd_date, fwd_src)


def new_media(media, message_id):
	if media is None:
		return None
	assert isinstance(media, dict)
	assert "type" in media
	if media["type"] == "geo":	# {'latitude': 53.779889, 'type': 'geo', 'longitude': -1.755313}
		assert "latitude" in media
		assert "longitude" in media
		return Location(TGL, message_id, media["latitude"], media["longitude"])
	elif media["type"] == "":
		pass
	elif media["type"] == "":
		pass
	else:
		logging.warning("Unhandled media type: {type}".format(type=media["type"]))
	if media is None:
		return None


def on_msg_receive(msg):
	print(msg)
	message = new_message(msg)
	print(message)


tgl.set_on_msg_receive(on_msg_receive)

