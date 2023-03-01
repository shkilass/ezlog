
<p align="center">
  <img src="https://github.com/ftdot/ezlog/blob/master/docs/source/present.png" />
</p>

# ezlog

[![Documentation](https://img.shields.io/readthedocs/ezlog?style=for-the-badge)](https://ezlog.readthedocs.io/)
[![Issues](https://img.shields.io/github/issues/ftdot/ezlog?style=for-the-badge)](https://github.com/ftdot/ezlog/issues)
[![Latest tag](https://img.shields.io/github/v/tag/ftdot/ezlog?style=for-the-badge)](https://github.com/ftdot/ezlog/tags)
[![PyPI](https://img.shields.io/pypi/v/ezloglib?style=for-the-badge)](https://pypi.org/project/ezloglib)
  
Modern, simple in use, colored logging library for python.

* Formatting support
* Stdout\\Stderr\\File handlers
* Easy to use & add custom handlers
* Colored and customizable


## Installation

You can install this via **pip** (Windows):

```sh
pip install ezloglib
```

And also for linux systems:

```sh
pip3 install ezloglib
```

Read more about this on the [documentation](https://ezlog.readthedocs.io/)


## Examples

Example from the [documentation](https://ezlog.readthedocs.io/).

File: [examples/presentation.py](examples/presentation.py)

```py

import ezlog
import math

# declare stdout handler with log level - debug
sout_handler = ezlog.StdoutHandler(log_level='debug')

# initialize main logger
main_logger = ezlog.Logger('Main', handlers=[sout_handler])

# examples of the default log levels
main_logger.debug('This is {} message', 'debug')
main_logger.exception('This is {} message', 'exception')
main_logger.info('This is {} message', 'info')
main_logger.warning('This is {} message', 'warning')
main_logger.error('This is {} message', 'error')
main_logger.critical('This is critical message')

# pretty formatting + colored types
main_logger.debug('Int: {} List: {} Dict: {}', 13, [1, 2, 3], {'hello': 'world'})
main_logger.exception('Tuple: {} Bool: {} Bytes: {}', ('hello', 'world'), True, b'whois?')
main_logger.info('Float: {}', math.pi)
main_logger.warning('Exception (color): {}', NameError("name 'abc' is not defined"))

# example of the formatting
main_logger.info('{:<20}--{:>19}', 'pi is', f'{math.pi:.2f}')

# example exception logging
try:
    printt('Hello, world!')
except Exception as e:
    # NOTE: You can use also debug, critical and other log levels to print exception
    main_logger.exception('Exception example', exception=e)

main_logger.info('It is continue work')
```

File: [examples/presentation.py](examples/groups_filelogging.py)

```py

import ezlog

# declare stdout handler with log level - debug
file_handler = ezlog.FileHandler('example.log', log_level='debug')
sout_handler = ezlog.StdoutHandler(log_level='info')  # recommended: exception log level as default

# initialize example groups
example_group = ezlog.LoggerGroup('Example', handlers=[sout_handler, file_handler])
groups_group = ezlog.LoggerGroup('Groups', parent=example_group)

main_logger = ezlog.Logger('Main', group=groups_group)

# examples of the default log levels
main_logger.debug('This is {} message', 'debug')
main_logger.exception('This is {} message', 'exception')
main_logger.info('This is {} message', 'info')
main_logger.warning('This is {} message', 'warning')
main_logger.error('This is {} message', 'error')
main_logger.critical('This is critical message')
```
