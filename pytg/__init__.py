# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import fcntl
import struct
from utils import start_pipeline

class TelegramError(Exception):
    pass

class Telegram(object):
    _proc, tgin = None, None
    _pipeline, _callables = None, []
    _buffer, _banner_found = '', False
    _ignore = ['> \n','>\n']
    ready = False

    def __init__(self, telegram, pubkey_file):
        self._tg = telegram
        self._pub = pubkey_file

    def register_pipeline(self, pipeline):
        self._pipeline = start_pipeline(pipeline)

    def register_callable(self, func, *args, **kwargs):
        self._callables.append([func, args, kwargs])

    def start(self):
        proc = subprocess.Popen([self._tg, '-R', '-k', self._pub], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
            self.ready = True
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

    def safe_quit(self):
        self._proc.communicate('safe_quit\n')
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

    def send_audio(self, peer, path):
        self.tgin.write(' '.join(['send_audio', peer, path]) + '\n')
        self.tgin.flush()

    def send_document(self, peer, path):
        self.tgin.write(' '.join(['send_document', peer, path]) + '\n')
        self.tgin.flush()

    def send_photo(self, peer, path):
        self.tgin.write(' '.join(['send_photo', peer, path]) + '\n')
        self.tgin.flush()

    def send_video(self, peer, path):
        self.tgin.write(' '.join(['send_video', peer, path]) + '\n')
        self.tgin.flush()

    def send_text(self, peer, path):
        self.tgin.write(' '.join(['send_text', peer, path]) + '\n')
        self.tgin.flush()

    def status_online(self):
        self.tgin.write('status_online\n')
        self.tgin.flush()

    def status_offline(self):
        self.tgin.write('status_offline\n')
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

    def contact_list(self):
        self.tgin.write('contact_list\n')
        self.tgin.flush()

    def whoami(self):
        if 'HOME' in os.environ:
            authfile = os.path.join(os.environ['HOME'], '.telegram', 'auth')
            if os.path.exists(authfile):
                with open(authfile, 'rb') as fh:
                    fh.seek(-4, 2)
                    myid = struct.unpack('<I', fh.read(4))[0]
                return str(myid)
            else:
                raise TelegramError("You have not registered telegram client")
        else:
            raise TelegramError("Undefined 'HOME' environment variable")
