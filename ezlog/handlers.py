"""
Defines main ezlog handlers
"""

import sys
import typing
from os import PathLike
from typing import TextIO

from .utils import LogLevel, level_names
from ._types import LogLevelType

__all__ = ['LoggerHandler', 'FileHandler', 'StdoutHandler', 'StderrHandler',]


class LoggerHandler:
    """Handler for any IO"""

    def __init__(self,
                 io: TextIO | None = None,
                 log_level: LogLevelType = LogLevel.NOTSET,
                 colors: bool = True,
                 exceptions: bool = True):
        """
        :param io: TextIO to handle
        :type io: TextIO
        :param log_level: Level of logging (by default is LogLevel.NOTSET)
        :type log_level: LogLevel | str
        :param colors: Enable colors for the handler
        :type colors: bool
        :param exceptions: Enable exception handling for this handler
        :type exceptions: bool
        """

        self.io          = io
        self.log_level   = log_level if isinstance(log_level, int) else {v: k for k, v in level_names.items()}[log_level.upper()]
        self.colors      = colors
        self.exceptions  = exceptions

    def write(self, text: str):
        """Writes given text to the IO if it doesn't equal to None

        :param text: Text to write into IO
        :type text: str
        """
        if self.io is None:
            return

        self.io.write(text)
        self.io.flush()

    def __del__(self):
        self.io.close()


class FileHandler(LoggerHandler):
    """Handle file for logging

    :ivar path: Path to the file
    :type path: PathLike[str] | str
    """

    def __init__(self,
                 path: PathLike[str] | str,
                 **kwargs: typing.Any):
        """
        :param path: Path to the file
        :type path: PathLike[str] | str
        :param kwargs: Key=value parameters for the LoggerHandler
        :type kwargs: typing.Any

        Parameters from the :class:`LoggerHandler`:

        :param io: TextIO to handle
        :type io: TextIO
        :param log_level: Level of logging (by default is LogLevel.NOTSET)
        :type log_level: LogLevelType
        :param colors: Enable colors for the handler
        :type colors: bool
        :param exceptions: Enable exception handling for this handler
        :type exceptions: bool
        """
        if 'colors' in kwargs:
            super().__init__(open(path, 'w'), **kwargs)
        else:
            super().__init__(open(path, 'w'), colors=False, **kwargs)

        self.path = path

    def __del__(self):
        self.io.close()


class StdoutHandler(LoggerHandler):
    """Handle stdout output (console output)"""

    def __init__(self,
                 **kwargs: typing.Any):
        """
        :param kwargs: Key=value parameters for the LoggerHandler
        :type kwargs: typing.Any

        Parameters from the :class:`LoggerHandler`:

        :param io: TextIO to handle
        :type io: TextIO
        :param log_level: Level of logging (by default is LogLevel.NOTSET)
        :type log_level: LogLevelType
        :param colors: Enable colors for the handler
        :type colors: bool
        :param exceptions: Enable exception handling for this handler
        :type exceptions: bool
        """
        super().__init__(sys.stdout, **kwargs)

    def __del__(self):
        pass


class StderrHandler(LoggerHandler):
    """Handle stderr output (console error output)"""

    def __init__(self,
                 **kwargs: typing.Any):
        """
        :param kwargs: Key=value parameters for the LoggerHandler
        :type kwargs: typing.Any

        Parameters from the :class:`LoggerHandler`:

        :param io: TextIO to handle
        :type io: TextIO
        :param log_level: Level of logging (by default is LogLevel.NOTSET)
        :type log_level: LogLevelType
        :param colors: Enable colors for the handler
        :type colors: bool
        :param exceptions: Enable exception handling for this handler
        :type exceptions: bool
        """
        super().__init__(sys.stderr, **kwargs)

    def __del__(self):
        pass
