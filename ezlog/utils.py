"""
Utilities of the logging library (such as LogLevel, level names, functions)
"""

import colorama
import typing
import inspect

from ._types import ColorSetType

if typing.TYPE_CHECKING:
    from .logger import Logger

__all__ = ['LogLevel', 'level_names', 'level_to_color', 'level_to_name',
           'type_to_color', 'register_log_level', 'make_logger_binding',
           'register_bindings']


# log levels
class LogLevel:
    """Stores levels of log"""

    DEBUG      = 1
    EXCEPTION  = 2
    INFO       = 5
    WARNING    = 10
    ERROR      = 15
    CRITICAL   = 20
    NOTSET     = 9999


# names of the log levels
level_names = {
    LogLevel.DEBUG:      'DEBUG',
    LogLevel.EXCEPTION:  'EXCEPTION',
    LogLevel.INFO:       'INFO',
    LogLevel.WARNING:    'WARNING',
    LogLevel.ERROR:      'ERROR',
    LogLevel.CRITICAL:   'CRITICAL',
    LogLevel.NOTSET:     'NOTSET'
}


# utilities

def level_to_color(level: int, color_set: ColorSetType) -> str:
    """Converts log level to color

    :param level: Int level to convert
    :param color_set: Color set from get the colors

    :returns: String color of the level if level is registered, otherwise empty string
    """

    if level in color_set['level']:
        return color_set['level'][level]

    return ''


def level_to_name(level: int) -> str:
    """Converts log level to str

    :param level: Level to convert

    :returns: Level as string or empty string if level is not registered
    """

    if level in level_names:
        return level_names[level]

    return ''


def type_to_color(type_: type | str, color_set: ColorSetType) -> str:
    """Converts type to the color

    :param type_: Type to convert
    :param color_set: Color set from get colors of the types

    :returns: String with color of the type or returns color_set['types']['all'] color
    """

    if type_ in color_set['types']:
        return color_set['types'][type_]

    return color_set['types']['all']


def register_log_level(level: int, level_name: str):
    """Registers new log level

    :param level: Int level to register
    :param level_name: Name of the level to register
    """

    setattr(LogLevel, level_name, level)
    level_names[level] = level_name


def make_logger_binding(level: int) -> ...:
    """Makes function bind to do record for the given log level

    :param level: Int level to bind
    :type level: int

    :returns: Bind function to log the given log level
    """

    def f(self: 'Logger', message: str, *args, exception: Exception | None = None):
        self.record(message, *args, level=level, exception=exception, stack=inspect.stack()[1])

    return f


def register_bindings(cls: 'Logger'):
    """Registers bindings for the levels to a Logger class

    :param cls: Class (must be Logger class)
    :type cls: Logger
    """

    # make bindings to the all log levels
    for level, name in level_names.items():
        name_l = name.lower()

        if getattr(cls, name_l, None) is not None:
            continue

        setattr(cls, name.lower(), make_logger_binding(level))
