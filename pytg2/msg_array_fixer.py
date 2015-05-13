__author__ = "luckydonald"
import logging
logger = logging.getLogger(__name__)
from .encoding import to_unicode as u


TGL_PEER_CHAT = u("chat")
TGL_PEER_USER = u("user")
TGL_PEER_ENCR_CHAT = u("encr_chat")
TGL_PEER_GEO_CHAT = u("geo_chat") #todo: does this even exists?

def fix_message(message):
	# skip if not has message typical elements
	if not all(key in message for key in ["from", "to", "out"]):
		return message

	# create the peer, thats where to reply to.
	if message["out"]:
		message["peer"] = None
	elif message["to"]["type"] == TGL_PEER_CHAT or message["to"]["type"] == TGL_PEER_GEO_CHAT:
		message["peer"] = message["to"]
	elif message["to"]["type"] == TGL_PEER_USER or message["to"]["type"] == TGL_PEER_ENCR_CHAT:
		message["peer"] = message["from"]

	# rename from -> sender
	message["sender"] = fix_peer(message["from"])
	del message["from"]

	# rename to -> receiver
	message["receiver"] = fix_peer(message["to"])
	del message["to"]

	# rename out -> own
	message["own"] = message["out"]
	del message["out"]

	# return it
	return message

def fix_peer(peer):
	# add cmd field
	peer["cmd"] = peer["type"] + u("#") + u(str(peer["id"]))

	# remove printnames like "user#123"
	if peer["print_name"] == peer["cmd"]:
		peer["print_name"] == None

	peer["name"] = (peer["name"]["first_name"] + peer["name"]["last_name"]) or peer["name"]["username"]
	return peer