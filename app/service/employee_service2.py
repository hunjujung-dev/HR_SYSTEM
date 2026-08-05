# app/services/employee_service.py


from datetime import datetime

from app.service.employee_validator import (
    EmployeeValidator
)

from app.models.employee import Employee


class EmployeeService:



    def __init__(
        self,
        db,
        employee_repo
    ):

        self.db = db

        self.employee_repo = employee_repo


    ##################################################
    # 직원 목록
    ##################################################

    def list(self):


        employees = (
            self.employee_repo
            .find_all()
        )


        return employees

    ################################################
    # 사원 등록
    ################################################

    def create_employee(
        self,
        data,
        photo=None,
        login_user=None
    ):


        # 1. 사번 중복 검사

        exists = (
            self.employee_repo
            .find_by_emp_no(
                data.emp_no
            )
        )


        if exists:
            raise Exception(
                "이미 존재하는 사번입니다."
            )



        # 2. 부서 검사


        dept = (
            self.department_repo
            .find_by_id(
                data.dept_id
            )
        )


        if not dept:
            raise Exception(
                "존재하지 않는 부서입니다."
            )



        # 3. 직급 검사


        position = (
            self.position_repo
            .find_by_id(
                data.position_id
            )
        )


        if not position:

            raise Exception(
                "존재하지 않는 직급입니다."
            )



        # 4. Validation


        EmployeeValidator.validate_email(
            data.email
        )


        EmployeeValidator.validate_mobile(
            data.mobile
        )


        EmployeeValidator.validate_date(
            data.join_date,
            data.retire_date
        )




        ################################################
        # 사진 저장
        ################################################

        photo_path = None


        if photo:

            photo_path = (
                self.file_service
                .save_employee_photo(
                    photo,
                    data.emp_no
                )
            )




        ################################################
        # Employee 저장
        ################################################


        employee = (
            self.employee_repo
            .create(
                data,
                photo_path
            )
        )


        ################################################
        # History 저장
        ################################################


        self.history_service.create(
            employee_id=
            employee.id,

            history_type="CREATE",

            before=None,

            after=data.dict(),

            reg_user=login_user
        )




        ################################################
        # Audit Log
        ################################################


        self.audit_service.write(

            user=login_user,

            action="EMPLOYEE_CREATE",

            target_id=employee.id,

            detail=data.dict()

        )



        self.db.commit()


        return employee
    

    ################################################
    # 사원 퇴사 처리
    ################################################
    def retire_employee(
            self,
            employee_id,
            retire_date,
            user
    ):

        employee = (
            self.employee_repo
            .find(employee_id)
        )


        if not employee:
            raise Exception(
                "사원을 찾을 수 없습니다."
            )

        before = employee.status

        employee.status = "RETIRE"

        employee.retire_date = retire_date



        self.history_service.create(
            employee_id,
            "RETIRE",
            {
                "status":before
            },

            {
                "status":"RETIRE"
            },

            user
        )



        self.audit_service.write(
            user,
            "EMPLOYEE_RETIRE",
            employee_id,
            {}
        )

        self.db.commit()

        return employee
    

    ################################################
    # 재직 상태 처리
    #   ACTIVE       재직
    #   LEAVE        휴직
    #   RETIRE       퇴사
    #   WAIT         입사예정
    ################################################
    def change_status(
        self,
        employee_id,
        status,
        user
    ):
        employee = (
            self.employee_repo
            .find(employee_id)
        )


        old_status = employee.status


        employee.status=status



        self.history_service.create(

            employee_id,

            "STATUS_CHANGE",

            {
                "status":old_status
            },

            {
                "status":status
            },

            user
        )


        self.db.commit()


        return employee