# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import logging
logger = logging.getLogger(__name__)

from luckydonaldUtils.encoding import to_unicode as u

ENCR_CHAT_PREFIX = "!_user@"
TGL_PEER_CHAT = u("chat")
TGL_PEER_USER = u("user")
TGL_PEER_ENCR_CHAT = u("encr_chat")
TGL_PEER_GEO_CHAT = u("geo_chat") #todo: does this even exists?
TGL_PEER_CHANNEL = u("channel")

def fix_message(message):
	# skip if not has message typical elements
	if not all(key in message for key in ["from", "to", "out"]):
		return message

	# rename from -> sender
	message["sender"] = fix_peer(message["from"])
	del message["from"]

	# rename to -> receiver
	message["receiver"] = fix_peer(message["to"])
	del message["to"]

	# rename out -> own
	message["own"] = message["out"]
	del message["out"]

	# create the peer, thats where to reply to.
	if message["own"]:
		message["peer"] = None
	elif message["receiver"]["type"] == TGL_PEER_CHAT or message["receiver"]["type"] == TGL_PEER_GEO_CHAT or message["receiver"]["type"] == TGL_PEER_CHANNEL:
		message["peer"] = message["receiver"]
	elif message["receiver"]["type"] == TGL_PEER_USER or message["receiver"]["type"] == TGL_PEER_ENCR_CHAT:
		message["peer"] = message["sender"]
	# return it
	return message


def fix_peer(peer):
	# rename peer_type => type
	if peer["peer_type"]:
		peer["type"] = peer["peer_type"]
		del peer["peer_type"]

	# add cmd field
	if peer["type"] == TGL_PEER_ENCR_CHAT:
		assert peer["print_name"].startswith(ENCR_CHAT_PREFIX)
		peer["cmd"] = peer["print_name"]
	elif peer["type"] == TGL_PEER_CHANNEL:
		peer["cmd"] = u("%s#id%d") % (peer["type"], peer["peer_id"])
	else:
		peer["cmd"] = u("%s#%d") % (peer["type"], peer["peer_id"])

	#remove print_name field
	#create name field
	if "print_name" in peer:
		peer["name"] = peer["print_name"] # just in case everything failes.
		del peer["print_name"] # can contain ugly print_names like "user#123", "chat#123" or "no_spaces_just_underscores"
	else:
		peer["name"] = ""

	#add name field
	if peer["type"] == TGL_PEER_USER:
		if "first_name" in peer and peer["first_name"]:
			peer["name"] = peer["first_name"]
		elif "username" in peer and peer["username"]:
			peer["name"] =  peer["username"]
	elif peer["type"] == TGL_PEER_CHAT or peer["type"] == TGL_PEER_CHANNEL:
		if "title" in peer and peer["title"]:
			peer["name"] = peer["title"]
	elif peer["type"] == TGL_PEER_ENCR_CHAT:
		if "user" in peer and peer["user"]:
			if "first_name" in peer and peer["first_name"]:
				peer["name"] = peer["first_name"]
			elif "username" in peer and peer["username"]:
				peer["name"] =  peer["username"]
			elif "print_name" in peer and peer["print_name"]:
				peer["name"] =  peer["username"] # there are no other choices.
	else:
		logger.error("Unknown peer type: {type}".format(type={peer["type"]}))
	return peer
