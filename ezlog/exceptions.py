
__all__ = ['StringGroupNotFoundException']


class StringGroupNotFoundException(Exception):
    """Exception raised when :class:`LoggerGroup` can't find given parent

    :ivar unknown_parent: Unknown string group parent
    :type unknown_parent: str
    """

    def __init__(self, unknown_parent: str):
        """
        :param unknown_parent: Unknown string group parent
        :type unknown_parent: str
        """
        super().__init__()

        self.unknown_parent = unknown_parent

    def __str__(self):
        return f'Unknown string group parent "{self.unknown_parent}"'
