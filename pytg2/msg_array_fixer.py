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
	elif message["receiver"]["type"] == TGL_PEER_CHAT or message["receiver"]["type"] == TGL_PEER_GEO_CHAT:
		message["peer"] = message["receiver"]
	elif message["receiver"]["type"] == TGL_PEER_USER or message["receiver"]["type"] == TGL_PEER_ENCR_CHAT:
		message["peer"] = message["sender"]


	# return it
	return message

def fix_peer(peer):
	# add cmd field
	peer["cmd"] = peer["type"] + u("#") + u(str(peer["id"]))

	# remove printnames like "user#123"
	if peer["print_name"] == peer["cmd"]:
		peer["print_name"] == None

	peer["name"] = (peer["first_name"] + peer["last_name"]) or peer["username"]
	return peer