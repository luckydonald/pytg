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
	while not _QUIT:
		time.sleep(1)
	print("wait   .3")

	return



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