# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import fcntl
from utils import start_pipeline

class TelegramError(Exception):
    pass

class Telegram(object):
    _proc, tgin = None, None
    _pipeline, _callables = None, []
    _buffer, _banner_found = '', False
    _ignore = ['...\n']

    def __init__(self, telegram, pubkey_file):
        self._tg = telegram
        self._pub = pubkey_file

    def register_pipeline(self, pipeline):
        self._pipeline = start_pipeline(pipeline)

    def register_callable(self, func, *args, **kwargs):
        self._callables.append([func, args, kwargs])

    def start(self):
        proc = subprocess.Popen([self._tg, '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self._proc, self.tgin = proc, proc.stdin
        fd = proc.stdout.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def poll(self):
        if not self._proc or self._proc.poll():
            raise TelegramError('telegram not running')

        try:
            c = self._proc.stdout.read(1)
        except:
            c = ''
        self._buffer += c
        if not self._banner_found and c == '\n' and 'conditions' in self._buffer:
            self._banner_found = True
            self.tgin.write('set msg_num 1\n')
            self.tgin.flush()
            self._buffer = ''
        if self._banner_found and c == '\n':
            if '{print_message}' in self._buffer:
                if '{end_print_message}' in self._buffer:
                    self._pipeline.send(self._buffer)
                    self._buffer = ''
            else:
                if self._buffer not in self._ignore:
                    self._pipeline.send(self._buffer)
                self._buffer = ''

    def quit(self):
        self._proc.communicate('quit\n')
        if len(self._buffer) > 0:
            self._pipeline.send(self._buffer)
        self._pipeline.close()

    def force_quit(self):
        try:
            pipeline.close()
        except:
            pass
        self._proc.terminate()

    def msg(self, peer, message):
        self.tgin.write(' '.join(['msg', peer, message]) + '\n')
        self.tgin.flush()

    def dialog_list(self):
        self.tgin.write('dialog_list\n')
        self.tgin.flush()

    def chat_info(self, chat):
        self.tgin.write(''.join(['chat_info ', chat, '\n']))
        self.tgin.flush()

    def user_info(self, user):
        self.tgin.write(''.join(['user_info ', user, '\n']))
        self.tgin.flush()

    def mark_read(self, peer):
        self.tgin.write(''.join(['mark_read ', peer, '\n']))
        self.tgin.flush()

    def chat_with_peer(self, peer):
        self.tgin.write(''.join(['chat_with_peer ', peer, '\n']))
        self.tgin.flush()
