# -*- coding: utf-8 -*-
import pytg

__author__ = 'luckydonald'

"""
    This is more a TEST, not an example...
    You probably should NOT start with this.
"""


def main():
    import signal
    signal.signal(signal.SIGINT, sigint_handler)
    tg = pytg.Telegram(telegram="/path/to/tg/bin/telegram-cli", pubkey_file="/path/to/tg/tg-server.pub")
    tg.stop_cli()

    import time
    print("Wait a bit (100s), you can test Ctrl-C here.")
    time.sleep(100)
    print("wait100.1")
    time.sleep(100)
    print("wait100.2")
    while not _QUIT:
        time.sleep(1)
    print("Quit it!")
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
                "\n [Ctrl-C]  Press again (in the next 3 seconds) to Continue.")
            _quitfirst = now
            return
        else:
            print("\n [Ctrl-C] Shutting down... Press again to force termination.")
            _quitfirst = now
            _QUIT = True
            return
    else:
        print("\n [Ctrl-C]  Termination. ")
        import sys  # only required once on runtime, lol.
        sys.exit()


if __name__ == '__main__':
    main()
    print("gone.")
