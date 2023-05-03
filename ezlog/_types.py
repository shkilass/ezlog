"""
Declares types of this logging library
"""

LogLevelType = int | str
ColorSetType = dict[str, dict[LogLevelType | type | str, str]]
