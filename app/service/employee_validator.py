# app/services/employee_validator.py

import re
from datetime import date


class EmployeeValidator:


    @staticmethod
    def validate_email(email):

        if not email:
            return True

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(pattern,email):
            raise Exception(
                "이메일 형식이 올바르지 않습니다."
            )

        return True



    @staticmethod
    def validate_mobile(phone):

        if not phone:
            return True


        pattern = r'^010-\d{4}-\d{4}$'


        if not re.match(pattern,phone):
            raise Exception(
                "휴대폰 번호 형식 오류"
            )

        return True



    @staticmethod
    def validate_date(
        join_date,
        retire_date
    ):


        if retire_date:

            if retire_date < join_date:
                raise Exception(
                    "퇴사일은 입사일 이후여야 합니다."
                )

        return True