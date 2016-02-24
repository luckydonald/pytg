# -*- coding: utf-8 -*-
import threading
import socket  # connect to telegram cli.
import json
import logging
from collections import deque
from types import GeneratorType
from errno import EINTR, ECONNREFUSED

from luckydonaldUtils.encoding import to_unicode as u
from luckydonaldUtils.encoding import to_binary as b
from luckydonaldUtils.encoding import to_native as n
from DictObject import DictObject

from .utils import coroutine
from . import fix_plain_output
from .exceptions import ConnectionError
from .fix_msg_array import fix_message

__author__ = 'luckydonald'

logger = logging.getLogger(__name__)

SOCKET_SIZE = 1 << 25
BLOCK_SIZE = 256

EMPTY_UNICODE_STRING = u("")  # So we don't call it every time in the if header.
EMPTY_RAW_BYTE = b("")  # So we don't call it every time in the if header.
_REGISTER_SESSION = b("main_session\n")
_ANSWER_SYNTAX = b("ANSWER ")
_LINE_BREAK = b("\n")


class Receiver(object):
    """
    Start telegram client somewhere.
    $ ./bin/telegram-cli -P 4458 -W --json
    Get a telegram
    >>> tg = Receiver()
    >>> tg.start()

    """
    _do_quit = False
    _queue = deque()
    _new_messages = threading.Semaphore(0)
    _queue_access = threading.Lock()

    def __init__(self, host="localhost", port=4458, append_json=False):
        """
        :param append_json: if the dict should contain the original json.
        """
        self.host = host
        self.port = port
        self.append_json = append_json
        self.s = None  # socket.

    def queued_messages(self):
        """
        Informs how many messages are still in the queue, waiting to be processed.

        :return: integer, the messages currently in queue.
        :rtype: int
        """
        with self._queue_access:
            return len(self._queue)

    def start(self):
        """
        Starts the receiver.
        When started, messages will be queued.
        :return:
        """
        self._receiver_thread = threading.Thread(name="Receiver (pytg)", target=self._receiver, args=())
        self._receiver_thread.daemon = True  # exit if script reaches end.
        self._receiver_thread.start()

    def stop(self):
        """
        Shuts down the receivers server.
        No more messages will be received.
        You should not try to start() it again afterwards.
        """
        self._do_quit = True
        if self.s:
            self.s.settimeout(0)
        if self.s:
            self.s.close()
        if hasattr(self, "_receiver_thread"):
            logger.debug("receiver thread existing: {}".format(self._receiver_thread.isAlive()))
        else:
            logger.debug("receiver thread existing: Not created.")
            # self._new_messages.release()

    def _receiver(self):
        while not self._do_quit:  # retry connection
            self.s = socket.socket()  # errors?
            try:
                self.s.connect((self.host, self.port))
            except socket.error as error:
                self.s.close()
                if error.errno == ECONNREFUSED and not self._do_quit:
                    continue
                raise error  # Not the error we are looking for, re-raise
            except Exception as error:
                self.s.close()
                raise error
            logger.debug("Socket Connected.")
            try:
                self.s.sendall(_REGISTER_SESSION)
            except Exception as error:
                self.s.close()
                raise error  # retry?
            logger.debug("CLI session registered.")
            buffer = EMPTY_RAW_BYTE
            answer = EMPTY_RAW_BYTE
            completed = -1  # -1 = answer size yet unknown, >0 = got remaining answer size
            while not self._do_quit:  # read loop
                while 1:  # retry if CTRL+C'd
                    try:
                        self.s.setblocking(True)
                        answer = self.s.recv(1)
                        # recv() returns an empty string if the remote end is closed
                        if len(answer) == 0:
                            self.s.close()
                            raise ConnectionError("Remote end closed.")
                        break
                    except socket.error as err:
                        if self._do_quit:
                            self.s.close()
                            return
                        if err.errno != EINTR:
                            raise
                        else:
                            logger.exception("Uncatched exception in reading answer from cli.")
                            self.s.close()
                            break  # to the retry connection look again.
                # end while: ctrl+c protection
                if completed == 0:
                    logger.debug("Hit end.")
                    if answer != _LINE_BREAK:
                        raise ValueError("Message does not end with a double linebreak.")
                    if buffer == EMPTY_RAW_BYTE:
                        logger.debug("skipping second linebreak.")
                        completed = -1
                        continue
                    logger.debug("Received Message: %s", buffer)
                    text = n(buffer)
                    if len(text) > 0 and text.strip() != "":
                        self._add_message(text)
                    else:
                        logger.warn("Striped text was empty.")
                    answer = EMPTY_RAW_BYTE
                    buffer = EMPTY_RAW_BYTE
                    # completed = 0 (unchanged)
                    continue
                buffer += answer
                # logger.debug("{!s:<2.2s}: {!s}".format(repr(answer)[1:-1]), buffer)# Fixed mallformatting of sting.
                if completed < -1 and buffer[:len(_ANSWER_SYNTAX)] != _ANSWER_SYNTAX[:len(buffer)]:
                    raise ArithmeticError("Server response does not fit. (Got >{}<)".format(buffer))
                if completed <= -1 and buffer.startswith(_ANSWER_SYNTAX) and buffer.endswith(_LINE_BREAK):
                    completed = int(n(buffer[len(_ANSWER_SYNTAX):-1]))  # TODO regex.
                    buffer = EMPTY_RAW_BYTE
                completed -= 1
            # end while: read loop
            if self.s:
                self.s.close()
                self.s = None
        # end while not ._do_quit: retry connection
        if self.s:
            self.s.close()
            self.s = None

    def _add_message(self, text):
        """
        Appends a message to the message queue.

        :type text: builtins.str
        :return:
        """
        try:
            logger.debug("Received Message: \"{str}\"".format(str=text))
            json_dict = json.loads(text)
            message = DictObject.objectify(json_dict)
            message = fix_message(message)
        except ValueError as e:
            for check in fix_plain_output.all:
                m = check[0].match(text)
                if m:
                    message = DictObject(manual_result=m.groupdict(), type=check[1])
                    logger.warn("Manually parsed output! This should be json!\nMessage:>{}<".format(text))
                    break
            else:
                logger.warn("Received message could not be parsed.\nMessage:>{}<".format(text), exc_info=True)
                return
        if self.append_json:
            message.merge_dict({u("json"): text})
        with self._queue_access:
            self._queue.append(message)
            self._new_messages.release()
    # end def

    @coroutine
    def message(self, function):
        if not isinstance(function, GeneratorType):
            raise TypeError('Target must be GeneratorType')
        try:
            while not self._do_quit:
                self._new_messages.acquire()  # waits until at least 1 message is in the queue.
                with self._queue_access:
                    message = self._queue.popleft()  # pop oldest item
                    logger.debug('Messages waiting in queue: %d', len(self._queue))
                function.send(message)
        except GeneratorExit:
            pass
        except KeyboardInterrupt:
            raise StopIteration
	# end def

# end class
