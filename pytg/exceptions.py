# -*- coding: utf-8 -*-
__author__ = 'luckydonald'
import logging

logger = logging.getLogger(__name__)


# sender.py
class NoResponse(Exception):
    pass


# sender.py
class ConnectionError(NoResponse):
    pass


# sender.py
class UnknownFunction(Exception):
    pass


# result_parser.py/sender.py
class IllegalResponseException(Exception):
    pass


# result_parser.py/sender.py
class FailException(IllegalResponseException):
    """
    Used when the cli sends somethhing like
    {'error_code': 100, 'result': 'FAIL', 'error': 'RPC_CALL_FAIL 400: USERNAME_INVALID'}

    This class has the following attributes:
    error_code, error and command.
    command could be None.
    """

    def __init__(self, error_code, error, command=None):
        """
        :param error_code: The error code returnded by the CLI.
        :type  error_code: int
        :param error: The message the CLI gives us.
        :type  error: str
        :keyword command: The command issued.
        :type    command: str | None
        """
        self.error_code = error_code
        self.error = error
        self.command = command
    # end def __init__

    def __str__(self, *args, **kwargs):
        formatter = "Error {code}: {error!r}" + (" (command {command!r})" if self.command else "")
        return formatter.format(command=self.command, code=self.error_code, error=self.error)
    # end def __str__
# end class


# argument_types.py
class ArgumentParseError(Exception):
    pass
