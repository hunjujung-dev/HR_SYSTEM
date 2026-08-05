from sqlalchemy.orm import Session

from app.models.employee import Employee



class EmployeeRepository:


    def __init__(
        self,
        db: Session
    ):

        self.db = db



    ##################################################
    # 사번 중복 검사
    ##################################################

    def exists_emp_no(
        self,
        emp_no
    ):

        return (
            self.db.query(Employee)
            .filter(
                Employee.emp_no == emp_no
            )
            .first()
            is not None
        )



    ##################################################
    # 로그인 ID 중복 검사
    ##################################################

    def exists_login_id(
        self,
        login_id
    ):

        return (
            self.db.query(Employee)
            .filter(
                Employee.login_id == login_id
            )
            .first()
            is not None
        )



    ##################################################
    # 단건 조회
    ##################################################

    def find(
        self,
        emp_id
    ):

        return (
            self.db.query(Employee)
            .filter(
                Employee.emp_id == emp_id
            )
            .first()
        )



    ##################################################
    # 전체 조회
    ##################################################

    def find_all(
        self
    ):

        return (

            self.db.query(Employee)

            .filter(
                Employee.use_yn == "Y"
            )

            .order_by(
                Employee.emp_id.desc()
            )

            .all()

        )



    ##################################################
    # 등록
    ##################################################

    def create(
        self,
        employee
    ):

        self.db.add(employee)

        self.db.flush()

        return employee



    ##################################################
    # 수정
    ##################################################

    def update(
        self,
        employee,
        data
    ):


        for key,value in data.model_dump(
            exclude_unset=True
        ).items():

            setattr(
                employee,
                key,
                value
            )


        self.db.flush()


        return employee



    ##################################################
    # 삭제(논리삭제)
    ##################################################

    def delete(
        self,
        employee
    ):

        employee.use_yn="N"

        self.db.flush()