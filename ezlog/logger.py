"""
Declares Logger - main class of this library.
"""

import colorama
import inspect
import traceback
from datetime import datetime
from typing import Any

from .utils import *
from ._types import ColorSetType
from .handlers import LoggerHandler
from .loggergroup import LoggerGroup, LOGGER_GROUPS
from .defaults import *

__all__ = ['DEFAULT_COLOR_SET', 'DEFAULT_FORMATTER', 'DEFAULT_TIME_FORMATTER',
           'LOGGER_GROUPS', 'reset', 'Logger']

# colors reset
reset = colorama.Style.RESET_ALL


class Logger:
    """Class of the Logger"""

    def __init__(self,
                 name: str,
                 formatter: str | None = None,
                 time_formatter: str | None = None,
                 color_set: ColorSetType | None = None,
                 handlers: list[LoggerHandler] | None = None,
                 group: LoggerGroup | str | None = None
                 ):
        """
        :param name: Name of the logger
        :type name: str
        :param formatter: String formatter of the record
        :type formatter: str | None
        :param time_formatter: String formatter for the time
        :type time_formatter: str
        :param color_set: Colors set to use (dict with the colors)
        :type color_set: ColorSetType
        :param handlers: Handlers (List with the LoggerHandler instances). It is using to write records in
        :type handlers: list[LoggerHandler]
        :param group: Group of the handler (Copy all values from)
        :type group: LoggerGroup | str | None
        """

        self.name = name

        if group is not None:
            # copy settings from the logger group

            if isinstance(group, str):
                group = LOGGER_GROUPS[group]

            self.group = group

            self.initialize_group()

        else:

            # register logger settings
            self.formatter       = formatter if formatter is not None else DEFAULT_FORMATTER
            self.time_formatter  = time_formatter if time_formatter is not None else DEFAULT_TIME_FORMATTER
            self.color_set       = color_set if color_set is not None else DEFAULT_COLOR_SET
            self.handlers        = handlers if handlers is not None else []

            self.group           = None

    def initialize_group(self):
        """Copy all settings from the group to itself"""

        self.formatter       = self.group.formatter
        self.time_formatter  = self.group.time_formatter
        self.color_set       = self.group.color_set
        self.handlers        = self.group.handlers

    def format_time(self, time: datetime) -> str:
        """Formats a time with time_formatter attribute

        :param time: Time to format
        :type time: datetime

        :returns: Formatted time
        :rtype: str
        """

        return self.time_formatter.format(year=time.year,
                                          month=time.month,
                                          day=time.day,
                                          hour=time.hour,
                                          minute=time.minute,
                                          second=time.second,
                                          microsecond=str(time.microsecond)[:4])

    def format_message(self, message: str, args_str: list[str], level_str: str, time_str: str, stack: inspect.FrameInfo) -> str:
        """Formats given message with formatter attribute

        :param message: Message to format
        :type message: str
        :param args_str: Arguments to format message with
        :type args_str: list[str]
        :param level_str: Level parameter
        :type level_str: str
        :param time_str: Time parameter
        :type time_str:
        :param stack: FrameInfo about caller of the log function
        :type stack: inspect.FrameInfo

        :returns: Formatter string
        :rtype: str
        """

        gname = self.group.group_link if self.group is not None else 'ezlog'

        return self.formatter.format(message=message.format(*args_str,
                                                            time=time_str,
                                                            name=self.name,
                                                            group_name=gname,
                                                            level=level_str,
                                                            foreground=colorama.Fore,
                                                            background=colorama.Back,
                                                            style=colorama.Style,
                                                            reset=reset,
                                                            stack=stack),
                                     time=time_str,
                                     name=self.name,
                                     group_name=gname,
                                     level=level_str,
                                     foreground=colorama.Fore,
                                     background=colorama.Back,
                                     style=colorama.Style,
                                     reset=reset,
                                     stack=stack
                                     )

    def record(self, message: str,
               *args: Any,
               level: int | str = LogLevel.NOTSET,
               exception: Exception | None = None,
               stack: inspect.FrameInfo | None = None):
        """Records a log to the handlers with formatters usage

        :param message: Message to record
        :type message: str
        :param args: Arguments to format with message
        :type args: Any
        :param level: Log level of the record
        :type level: int | str
        :param exception: Exception (if haven) to log
        :type exception: Exception | None
        :param stack: FrameInfo about caller of the log function
        :type stack: inspect.FrameInfo
        """

        if stack is None:
            stack = inspect.stack()[1]

        # get formatted time
        time_str = self.format_time(datetime.now())

        # get colored args\text
        args_str      = [str(o) for o in args]
        args_colored  = [type_to_color(type(o), self.color_set) + str(o) + reset for o in args]

        level_str      = level_to_name(level)
        level_colored  = level_to_color(level, self.color_set) + level_str + reset

        message_colored = message
        if level == LogLevel.CRITICAL:
            message_colored = f'{colorama.Back.LIGHTRED_EX}{colorama.Fore.BLACK}{message}{reset}'

        # get formatted message
        f_message          = self.format_message(message, args_str, level_str, time_str, stack)
        f_message_colored  = self.format_message(message_colored, args_colored, level_colored, time_str, stack) + reset

        # write record to the handlers
        for h in self.handlers:
            if h.log_level <= level:
                h.write((f_message_colored if h.colors else f_message) + '\n')

                if exception is not None and h.exceptions:
                    # get color for the exception
                    exception_color = type_to_color('exception', self.color_set) if h.colors else ''

                    h.write(exception_color + ''.join(traceback.format_exception(exception))[:-1] + reset + '\n')

    def debug(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as DEBUG.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def exception(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as EXCEPTION.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def info(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as INFO.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def warning(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as WARNING.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def error(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as ERROR.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def critical(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as CRITICAL.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

    def notset(self, message: str, *args: Any, exception: Exception | None = None):
        """Logs a message as NOTSET. There is no practical usage.

        :param message: Message to log
        :type message: str
        :param args: Packed arguments, that be formatted via ``str.format``
        :type args: Any
        :param exception: Exception to log (if any)
        :type exception: Exception | None
        """
        ...

# register bindings
register_bindings(Logger)
