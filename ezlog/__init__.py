"""
Small simple colored logging library
"""

import colorama
import sys

# Fix colors for the windows
if sys.platform == 'win32':
    colorama.just_fix_windows_console()
    colorama.init()

####

from .logger import *
from .loggergroup import *
from .handlers import *
from .utils import LogLevel
from . import utils, _types, defaults, exceptions
