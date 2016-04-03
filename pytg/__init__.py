# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

import atexit
import logging
from time import sleep

from .exceptions import NoResponse, IllegalResponseException
from luckydonaldUtils.encoding import to_unicode as u

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

__all__ = ["receiver", "sender", "Telegram"]
VERSION = "0.4.10"
__version__ = VERSION  # PEP-0396


class Telegram(object):
    """
    To have the sender and the receiver in one handsome object.
    Also is able to start the CLI, and stop it respectivly.
    """

    def __init__(self, host="127.0.0.1", port=4458, telegram=None, pubkey_file=None, custom_cli_args=None):
        from .sender import Sender
        from .receiver import Receiver
        self._proc = None
        if telegram and pubkey_file:
            if host not in ["127.0.0.1", "localhost", "", None]:
                raise ValueError("Can only start the cli at localhost. You may not provide a different host.")
            host = "127.0.0.1"
            self.start_cli(telegram=telegram, pubkey_file=pubkey_file, custom_cli_args=custom_cli_args, port=port)
        elif telegram is not None or pubkey_file is not None or custom_cli_args is not None:
            logger.warn("cli related parameter given, but not cli and pubkey path not present.")
        self.sender = Sender(host=host, port=port)
        self.receiver = Receiver(host=host, port=port)

        while self._proc is not None and self._proc.returncode is None:
            self._proc.poll()
            try:
                result = self.sender.raw(u("help"), retry_connect=False)
                if result and u("Prints this help") in result:
                    logger.info("CLI available.")
                else:
                    logger.warn("CLI does not responde correctly. (Debug: {})".format(result))
                break
            except:
                logger.info("CLI did not responde.")
            sleep(1)
        else:
            raise AssertionError("CLI Process died.")

    def start_cli(self, telegram=None, pubkey_file=None, custom_cli_args=None, port=4458):
        """
        Start the telegram process.

        :type port: int
        :type telegram: builtins.str
        :type pubkey_file: builtins.str
        :type custom_cli_args: list | tuple
        :return: (int) process id of telegram.
        :rtype int:
        """
        if not telegram or not pubkey_file:
            raise ValueError("telegram and/or pubkey_file not defined.")
        # TODO: Check if paths exist
        self._tg_cli = telegram
        self._public_key_file = pubkey_file
        import subprocess
        def preexec_function():
            import os
            os.setpgrp()

        atexit.register(self.stop_cli)
        args = [
            self._tg_cli, '-R', '-W', '-P', str(port),
            '-k', self._public_key_file, '--json',
            '--permanent-peer-ids', '--permanent-peer-ids',
        ]
        if custom_cli_args is not None:
            if not isinstance(custom_cli_args, (list, tuple)):
                raise TypeError("custom_cli_args should be a list or a tuple.")
            args.extend(custom_cli_args)
        logger.info("Starting Telegram Executable: \"{cmd}\"".format(cmd=" ".join(args)))
        self._proc = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=preexec_function)
        if self._check_stopped():
            raise AssertionError("CLI did stop, should be running...")
            # return pid
            # raise NotImplementedError("I Have to figure out processes in Python first...")
    startCLI = start_cli  # compatibility with <= v0.4.5

    def stop_cli(self):
        """
        Stop the telegram process.

        :return: (int) returncode of the cli process.
        :rtype int:
        """
        logger.info("Closing Connections.")
        logger.debug("Closing sender.")
        if self.sender:
            self.sender.terminate()  # not let the cli end close first -> avoid bind: port already in use.
        logger.debug("Closing sender.")
        if self.receiver:
            self.receiver.stop()
        logger.info("Asking to CLI to stop.")
        if self._proc is not None:
            if self.sender.do_quit:
                logger.debug("Sender already stopped. Unable to issue safe_quit or quit to exit via socket.")
            else:
                try:
                    self.sender.safe_quit()
                except (NoResponse, IllegalResponseException, AssertionError):
                    logger.debug("safe_quit Exception", exc_info=True)
                if self._check_stopped(): return self._proc.returncode
                logger.debug("safe_quit did not terminate.")

                try:
                    self.sender.quit()
                except (NoResponse, IllegalResponseException, AssertionError):
                    logger.debug("quit Exception", exc_info=True)
                if self._check_stopped(): return self._proc.returncode
                logger.debug("quit did not terminate.")
                self.sender.stop()  # quit and safe quit are done, we don't need the sender any longer.
            # end if-else: self.sender._do_quit
            if self._check_stopped(): return self._proc.returncode
            # has not terminated yet.
            self._proc.communicate('quit\n')  # report this error in the bugtracker!
            if self._check_stopped(): return self._proc.returncode
            try:
                self._proc.terminate()
            except Exception as e:  # todo: ProcessLookupError does not exist before python 3
                logger.debug("terminate Exception", exc_info=True)
            if self._check_stopped(): return self._proc.returncode
            logger.debug("terminate did not terminate.")

            try:
                self._proc.kill()
            except Exception as e:  # todo:  ProcessLookupError does not exist before python 3
                logger.debug("kill Exception", exc_info=True)
            if self._check_stopped(): return self._proc.returncode
            logger.debug("kill did not terminate.")
            logger.warn("CLI kinda didn't die... Will wait (block) for termination.")

            self._proc.wait()
            self._check_stopped()
            return self._proc.returncode
        else:
            logger.warn("No CLI running.")
            raise AssertionError("No CLI running.")
    stopCLI = stop_cli  # compatibility with <= v0.4.5

    def _check_stopped(self):
        self._proc.poll()
        if self._proc.returncode is not None:
            logger.info("CLI did stop ({return_code}).".format(return_code=self._proc.returncode))
            if hasattr(self, "sender") and self.sender is not None:
                self.sender.stop()
            return True
