.. _firststeps:

.. currentmodule:: ezlog

===========
First steps
===========

To install this library, simply type this command (Windows variant):

.. code-block:: shell

    pip install ezloglib

On linux systems, you must use ``pip3`` instead of. Command:

.. code-block:: shell

    pip3 install ezloglib

First handlers
--------------

To create a handler for the stdout (console output) you can use
:class:`ezlog.handlers.StdoutHandler`.

.. code-block:: python

    import ezlog

    # NOTE: Exception is a log level little than info.
    #       It recommended to use it for exception logging.
    lh_stdout = ezlog.StdoutHandler(log_level='exception')

.. note:: You can also use :class:`ezlog.utils.LogLevel` to set the ``log_level``
    parameter.

There also have support for **file handler**. This class named as
:class:`ezlog.handlers.FileHandler`.

.. code-block:: python

    import ezlog

    # NOTE: Sorry, for now there is no file date formatting by default :(
    #       I plan to add this in the future versions.
    lh_file = ezlog.FileHandler('mylog.txt', log_level='debug')

Lets combine them into one code:

.. code-block:: python

    import ezlog

    lh_stdout = ezlog.StdoutHandler(log_level='exception')
    lh_file = ezlog.FileHandler('mylog.txt', log_level='debug')

Our first handlers are done.

First logger group
------------------

Lets create our first logger group. Group contains all parameters for child
loggers. This is useful in case of multiple loggers usage. To create it, you
can use :class:`ezlog.loggergroup.LoggerGroup`

Create **MyApp** group:

.. code-block:: python

    import ezlog

    lg_myapp = ezlog.LoggerGroup('MyApp')

.. seealso:: You can see it reference: :class:`ezlog.loggergroup.LoggerGroup`

Lets add our loggers by examples above to this group.

.. note:: Handlers to the group can be pinned by ``handlers`` parameter.
    This parameter is named and takes ``list[LoggerHandler]`` type.
    Example is bottom.

.. code-block:: python

    import ezlog

    # Our first handlers for stdout and file
    lh_stdout = ezlog.StdoutHandler(log_level='exception')
    lh_file = ezlog.FileHandler('mylog.txt', log_level='debug')

    # Our first group by name MyApp
    lg_myapp = ezlog.LoggerGroup('MyApp', handlers=[lh_stdout, lh_file])

Our first group done!

First logger and log messages
-----------------------------

Loggers can be created by :class:`ezlog.logger.Logger` class. It, how as a
logger groups, takes a ``handlers`` parameter. But, as I said, if you use
logger group, it stores all parameters for child loggers and set it automatically.
All that required from Loggers is a ``group`` parameter. To get more info
see Loggers reference (just click on :class:`ezlog.logger.Logger`).

.. code-block:: python

    import ezlog

    # Our first handlers for stdout and file
    lh_stdout = ezlog.StdoutHandler(log_level='exception')
    lh_file = ezlog.FileHandler('mylog.txt', log_level='debug')

    # Our first group by name MyApp
    lg_myapp = ezlog.LoggerGroup('MyApp', handlers=[lh_stdout, lh_file])

    # Create a Main logger that includes MyApp group
    logger_main = ezlog.Logger('Main', group=)

Our logger is done! Now, we can log messages to it. By default, logger
hasn't ``debug`, ``exception``, ``info``` and other methods. It adds via
:func:`ezlog.utils.register_bindings()`. This methods calls by default,
and adds this list of the log levels (it defined in ``ezlog.utils.level_names``).

List of all default log levels:

* debug      (int value: ``1``)
* exception  (int value: ``2``)
* info       (int value: ``5``)
* warning    (int value: ``10``)
* error      (int value: ``15``)
* critical   (int value: ``20``)
* notset     (int value: ``9999``)

.. code-block:: python

    number1 = 15
    logger_main.debug('Defined number 1: {}', number1)

    number2 = 2
    logger_main.debug('Defined number 2: {}', number2)

    result = number1 + number2
    logger_main.info('Adding number 1 to number2. Result: {}', result)

.. note:: To log methods you can pass format variables as long as you need.

You can also use all features of the python string formatting.

.. warning:: All

.. code-block:: python

    import math

    logger_main.info('{:<20}--{:>19}', 'pi is', f'{math.pi:.2f}')

Code above fill produce info log with message: ``PI number is 3.14``.

Log exceptions
--------------

All methods of logging are defines named parameter ``exception=``. It
takes any exception and log it after the message.

.. code-block:: python

    try:
        printt('Hello, world!')
    except Exception as e:
        # You can use any function to log exception. But, recommended to use
        # only exception level for exceptions.

        logger_main.debug('An exception occurred: {}', e, exception=e)
        logger_main.exception('An exception occurred: {}', e, exception=e)
        logger_main.info('An exception occurred: {}', e, exception=e)
        logger_main.warning('An exception occurred: {}', e, exception=e)
        logger_main.error('An exception occurred: {}', e, exception=e)

        # There isn't recommended to use colored formatting with CRITICAL,
        # because it breaks colors.
        logger_main.critical(f'An exception occurred: {e}', exception=e)
