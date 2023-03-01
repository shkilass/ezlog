"""
Defines default variables, such as a color set
"""

import colorama

from ._types import ColorSetType
from .utils import LogLevel

__all__ = ['DEFAULT_COLOR_SET', 'DEFAULT_FORMATTER', 'DEFAULT_TIME_FORMATTER']

# default color set
DEFAULT_COLOR_SET: ColorSetType = {
    'level': {
        LogLevel.DEBUG:      colorama.Fore.LIGHTWHITE_EX,
        LogLevel.EXCEPTION:  colorama.Fore.LIGHTYELLOW_EX,
        LogLevel.INFO:       colorama.Fore.LIGHTCYAN_EX,
        LogLevel.WARNING:    colorama.Fore.YELLOW,
        LogLevel.ERROR:      colorama.Fore.LIGHTRED_EX,
        LogLevel.CRITICAL:   colorama.Fore.RED
    },
    'types': {
        int:          colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT,
        float:        colorama.Fore.LIGHTCYAN_EX,
        bool:         colorama.Fore.YELLOW,
        str:          colorama.Fore.LIGHTMAGENTA_EX + colorama.Style.BRIGHT,
        bytes:        colorama.Fore.LIGHTMAGENTA_EX,
        list:         colorama.Fore.LIGHTYELLOW_EX + colorama.Style.BRIGHT,
        tuple:        colorama.Fore.MAGENTA,
        Exception:    colorama.Fore.LIGHTRED_EX,
        'exception':  colorama.Fore.LIGHTRED_EX,
        'all':        colorama.Fore.LIGHTGREEN_EX + colorama.Style.BRIGHT
    }
}
"""Default color set"""

# default formatters
DEFAULT_FORMATTER       = '{time} | {level:<18} | {group_name:<18} -> {name:<18} — {message} — ln:{stack.lineno} fn:{stack.function}'
"""Default formatter of the record message"""

DEFAULT_TIME_FORMATTER  = '{year:04d}.{month:02d}.{day:02d} {hour:02d}:{minute:02d}:{second:02d}.{microsecond:04s}'
"""Default formatter of the time"""
