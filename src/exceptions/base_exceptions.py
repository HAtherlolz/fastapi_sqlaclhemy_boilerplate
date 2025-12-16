"""
The file contains the base exception class for handling processing errors in the application.
"""


class BaseAppException(Exception):
    status_code: int
    message: str

    def init(self, message: str | None = None):
        if message:
            self.message = message
        super().__init__(self.message)
