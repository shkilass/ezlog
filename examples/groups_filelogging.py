
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
