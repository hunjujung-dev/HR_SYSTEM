import re

from app.core.exception import ValidateException

class Validator:

    @staticmethod
    def required(value, message):

        if value is None:
            raise ValidateException(message)

        if isinstance(value, str):

            if value.strip() == "":
                raise ValidateException(message)

    @staticmethod
    def max_length(value, length, message):

        if value is None:
            return

        if len(value) > length:
            raise ValidateException(message)

    @staticmethod
    def min_length(value, length, message):

        if value is None:
            return

        if len(value) < length:
            raise ValidateException(message)

    @staticmethod
    def email(value):

        if value is None:
            return

        pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'

        if re.match(pattern, value) is None:

            raise ValidateException("이메일 형식이 아닙니다.")

    @staticmethod
    def phone(value):

        if value is None:
            return

        pattern = r'^[0-9\-]+$'

        if re.match(pattern, value) is None:

            raise ValidateException("전화번호 형식이 아닙니다.")

    @staticmethod
    def number(value):

        if value is None:
            return

        try:

            float(value)

        except:

            raise ValidateException("숫자만 입력 가능합니다.")