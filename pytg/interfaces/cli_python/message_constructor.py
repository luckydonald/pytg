# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging

logger = logging.getLogger(__name__)
import tgl
import sys

logging.basicConfig(level=logging.DEBUG)

from ...types import Message, Forward, User, Chat, Peer, UserStatus, Location, TGL, Reply
from ..access import MessageConstructorSuperclass


class MessageConstructor(MessageConstructorSuperclass):
	
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
		return UserStatus(TGL, user_status["online"], user_status["when"])
	
	
	def new_peer(self, peer):
		assert isinstance(peer, tgl.Peer)
		if peer.type_name == Peer.USER:
			return User(TGL, peer.id, peer.name, peer.first_name, peer.last_name, peer.phone, peer.username, self.new_userstatus(peer.user_status))
		elif peer.type_name == Peer.CHAT:
			return Chat(TGL, peer.id * (-1), peer.name, peer.user_list, peer.user_num, 0)
	
	
	def new_reply(self, id, message):
		if id is None:
			return None
		return Reply(TGL, id, message)
	
	
	def new_message(self, msg, queued_events):
		if msg == None:
			logging.debug("Message was None.")
			return None
		assert isinstance(msg, tgl.Msg)
		return Message(TGL, msg.id, msg.date, self.new_peer(msg.src), self.new_peer(msg.dest), msg.out, msg.mention, msg.unread,
					   msg.service, msg.flags, queued_events, fwd=self.new_fwd(msg.fwd_date, msg.fwd_src), reply=self.new_reply(msg.reply_id,msg.reply),
					   media=self.new_media(msg.media, msg.id), text=msg.text)
	
	
	def new_fwd(self, fwd_date, fwd_src):
		return Forward(TGL, fwd_date, fwd_src)

	def new_event(self, raw_event, queued_events):
		try:
			if isinstance(raw_event, tgl.Msg):
				return self.new_message(raw_event, queued_events)
			else:
				raise NotImplementedError("event type {t} is undefined.".format(t=type(raw_event)))
		except:
			logger.exception("Event {e} is type {t}".format(t=type(raw_event),e=raw_event))

	def new_media(self, media, message_id):
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
