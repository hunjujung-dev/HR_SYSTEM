class HRException(Exception):

    def __init__(self, message):

        self.message = message

        super().__init__(message)


class DuplicateException(HRException):
    pass


class NotFoundException(HRException):
    pass


class ValidateException(HRException):
    pass