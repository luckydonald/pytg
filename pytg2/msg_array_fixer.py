__author__ = "luckydonald"
import logging
logger = logging.getLogger(__name__)




def fix_message(message):
	if "from" in message:
		message["sender"] = message["from"]
		del message["from"]
	if "to" in message:
		message["receiver"] = message["to"]
		del message["to"]
	if "out" in message:
		message["own"] = message["out"]
		del message["out"]
	return message