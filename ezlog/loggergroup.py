
import typing

from .handlers import LoggerHandler
from ._types import ColorSetType
from .exceptions import StringGroupNotFoundException
from .defaults import *

if typing.TYPE_CHECKING:
    from .logger import Logger

__all__ = ['LoggerGroup', 'LOGGER_GROUPS']

# logger groups
LOGGER_GROUPS = {}


class LoggerGroup:
    """Group of loggers has shared parameters.
       Is highly recommended to create root logger and after pin all others logger to it
    """

    def __init__(self,
                 name: str,
                 parent: typing.Union['LoggerGroup', None] = None,
                 formatter: str | None = None,
                 time_formatter: str | None = None,
                 color_set: ColorSetType | None = None,
                 handlers: list[LoggerHandler] | None = None,
                 loggers: list['Logger'] | None = None
                 ):
        """

        :param name: Name of the group
        :type name: str
        :param parent: Parent of this group
        :type parent: LoggerGroup | None
        :param formatter: Formatter for the logs
        :type formatter: str | None
        :param time_formatter: Formatter for the time
        :type time_formatter: str | None
        :param color_set: Set of the colors to use
        :type color_set: ColorSetType | None
        :param handlers: Handlers, used to write all logs into
        :type handlers: list[LoggerHandler] | None
        :param loggers: Loggers to be pinned to this group
        :type loggers: list[Logger] | None

        :raises StringGroupNotFoundException: When string parent group not found
        """
        self.name = name

        if parent is None:
            self.formatter       = formatter if formatter is not None else DEFAULT_FORMATTER
            self.time_formatter  = time_formatter if time_formatter is not None else DEFAULT_TIME_FORMATTER
            self.color_set       = color_set if color_set is not None else DEFAULT_COLOR_SET
            self.handlers        = handlers if handlers is not None else []
            self.group_link      = self.name

        else:

            if isinstance(parent, str):
                if parent not in LOGGER_GROUPS:
                    raise StringGroupNotFoundException(parent)

                parent = LOGGER_GROUPS[parent]

            self.formatter       = parent.formatter
            self.time_formatter  = parent.time_formatter
            self.color_set       = parent.color_set
            self.handlers        = parent.handlers
            self.group_link      = '.'.join([parent.group_link, self.name])

        if isinstance(loggers, list):
            self.loggers = loggers

            # initialize all loggers
            for logger in self.loggers:
                logger.group = self
                logger.initialize_group()

        LOGGER_GROUPS[name] = self
