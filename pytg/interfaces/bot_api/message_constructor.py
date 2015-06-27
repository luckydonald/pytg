# -*- coding: utf-8 -*-
from datetime import datetime

__author__ = 'luckydonald'

import logging

logger = logging.getLogger(__name__)
import sys

logging.basicConfig(level=logging.DEBUG)

from ...types import Message, Forward, User, Chat, Peer, UserStatus, Location, Reply
from ...types import BOT_API_POLL as BOT_API_POLL
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
		return UserStatus(BOT_API_POLL, user_status["online"], user_status["when"])
	
	
	def new_peer(self, peer):
		assert peer["id"] != 0
		if peer["id"] > 0:
			return User(BOT_API_POLL,
						peer["id"],
						peer["first_name"],
						peer["first_name"],
						peer["last_name"] if "last_name" in peer else None,
						None,
						peer["username"] if "username" in peer else None,
						None)
		elif peer.type_name == Peer.CHAT:
			return Chat(BOT_API_POLL,
						peer["id"],
						peer["title"],
						[], None, 0)
	
	
	def new_reply(self, id, message):
		if id is None:
			return None
		return Reply(BOT_API_POLL, id, message)
	
	
	def new_message(self, msg, queued_events):
		if msg == None:
			logging.debug("Message was None.")
			return None
		receiver = self.new_peer(msg["chat"]) if "chat" in msg else None
		sender =  self.new_peer(msg["from"]) if "from" in msg else None
		reply = self.new_reply(msg["reply_to_message"]["id"],msg["reply_to_message"]) if "reply_to_message" in msg else None
		forward = self.new_fwd(self.new_time(msg["forward_date"]), msg["forward_from"]) if "reply_to_message" in msg else None
		media = None
		id =  msg["message_id"]
		if "location" in msg:
			media = Location(BOT_API_POLL, id, msg["location"]["latitude"], msg["location"]["longitude"])
		else:
			raise NotImplementedError("Other tyes not implemented.")
		text = msg["text"] if "text" in msg else None
		return Message(BOT_API_POLL, msg["message_id"], msg["date"], sender, receiver, False, None, True,
					   False, 0, queued_events, fwd=forward, reply=reply,
					   media=media, text=text)
	
	
	def new_fwd(self, fwd_date, fwd_src):
		return Forward(BOT_API_POLL, fwd_date, fwd_src)

	def new_event(self, raw_event, queued_events):
		if "message" in raw_event:
			return self.new_message(raw_event["message"], queued_events)
		else:
			try:
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
			return Location(BOT_API_POLL, message_id, media["latitude"], media["longitude"])
		elif media["type"] == "":
			pass
		elif media["type"] == "":
			pass
		else:
			logging.warning("Unhandled media type: {type}".format(type=media["type"]))
		if media is None:
			return None

	def new_time(self, unix_time):
		return datetime.fromtimestamp(unix_time)
