__author__ = 'luckydonald'

import pytg2





def main():
	import signal
	signal.signal(signal.SIGINT, sigint_handler)
	tg = pytg2.Telegram(telegram="/Users/tasso/git/tg/bin/telegram-cli", pubkey_file="/Users/tasso/git/tg/tg-server.pub")
	try:
		tg.sender.send_msg(u"luckydonald", u"test_")
	except pytg2.sender.NoResponse:
		pass
	import time
	print("wait100.0")
	time.sleep(100)
	print("wait100.1")
	time.sleep(100)
	print("wait100.2")
	raise False
	return
	tg.sender.get_contact_list()
	tg.sender.get_dialog_list()
	tg.sender.rename_chat()
	tg.sender.send_msg()
	tg.sender.send_typing()
	tg.sender.send_typing_abort()
	tg.sender.send_photo()
	tg.sender.send_video()
	tg.sender.send_audio()
	tg.sender.send_document()
	tg.sender.send_file()
	tg.sender.send_text()
	tg.sender.send_location()
	tg.sender.load_photo()
	tg.sender.load_video()
	tg.sender.load_video_thumb()
	tg.sender.load_audio()
	tg.sender.load_document()
	tg.sender.load_document_thumb()
	tg.sender.fwd_msg()
	tg.sender.fwd_media()
	tg.sender.chat_info()
	tg.sender.chat_set_photo()
	tg.sender.chat_add_user()
	tg.sender.chat_del_user()
	tg.sender.create_secret_chat()
	tg.sender.create_group_chat()
	tg.sender.user_info()
	tg.sender.get_history()
	tg.sender.add_contact()
	tg.sender.del_contact()
	tg.sender.rename_contact()
	tg.sender.msg_search()
	tg.sender.msg_global_search()
	tg.sender.mark_read()
	tg.sender.set_profile_photo()
	tg.sender.set_profile_name()
	tg.sender.delete_msg()
	tg.sender.restore_msg()
	tg.sender.accept_secret_chat()
	tg.sender.send_contact()
	tg.sender.status_online()
	tg.sender.status_offline()
	tg.sender.quit()
	tg.sender.safe_quit()
	tg.stopCLI()



_QUIT = False
_quitfirst = None
def sigint_handler(signum, frame):
		global _quitfirst, _QUIT
		from datetime import timedelta
		_quitdelta = timedelta(seconds=3)
		from datetime import datetime
		now = datetime.now()
		if not _QUIT:
			if (not _quitfirst or (now - _quitfirst) >= _quitdelta):
				print(
					"\n [Ctrl-C]  Press again to Continue.")
				_quitfirst = now
				return
			else:
				print("\n [Ctrl-C] Shutting down... Press again to force termination.")
				_quitfirst = now
				_QUIT = True
				return
		else:
			print("\n [Ctrl-C]  Termination. ")
			import sys #only required once on runtime, lol.
			sys.exit()



if __name__ == '__main__':
	main()
	print("gone.")