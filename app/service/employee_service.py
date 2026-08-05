from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.employee import Employee
from app.repository.employee_repository import EmployeeRepository


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


class EmployeeService:

    ############################################################
    # 직원목록
    ############################################################
    @staticmethod
    def list(
            db: Session,
            emp_no="",
            emp_name="",
            dept_cd="",
            status=""
    ):

        rows = EmployeeRepository.list(
            db,
            emp_no,
            emp_name,
            dept_cd,
            status
        )

        result = []

        for r in rows:

            result.append({
                "emp_id": r.emp_id,
                "emp_no": r.emp_no,
                "login_id": r.login_id,
                "emp_name": r.emp_name,
                "dept_cd": r.dept_cd,
                "position_cd": r.position_cd,
                "duty_cd": r.duty_cd,
                "phone": r.phone,
                "email": r.email,
                "join_date":
                    r.join_date.strftime("%Y-%m-%d")
                    if r.join_date else "",
                "status": r.status,
                "use_yn": r.use_yn,
                "company_id": r.company_id,
                "loc_code": r.loc_code
            })

        return result

    ############################################################
    # 직원조회
    ############################################################
    @staticmethod
    def get(
            db: Session,
            emp_id: int
    ):

        row = EmployeeRepository.get(
            db,
            emp_id
        )

        if row is None:

            return None

        return {
            "emp_id": row.emp_id,
            "emp_no": row.emp_no,
            "login_id": row.login_id,
            "emp_name": row.emp_name,
            "dept_cd": row.dept_cd,
            "position_cd": row.position_cd,
            "duty_cd": row.duty_cd,
            "phone": row.phone,
            "email": row.email,
            "join_date":
                row.join_date.strftime("%Y-%m-%d")
                if row.join_date else "",
            "status": row.status,
            "use_yn": row.use_yn,
            "company_id": row.company_id,
            "loc_code": row.loc_code
        }

    ############################################################
    # 직원등록
    ############################################################
    @staticmethod
    def create(
            db: Session,
            data
    ):
        

        # 사번 중복체크
        rows = EmployeeRepository.list(
            db,
            emp_no=data.emp_no
        )

        if len(rows) > 0:

            raise Exception("이미 존재하는 코드입니다.")

        # 로그인ID 중복체크
        query = db.query(Employee).filter(
            Employee.login_id == data.login_id
        ).first()

        if query:

            raise Exception("이미 존재하는 로그인ID입니다.")

        employee = Employee()

        employee.emp_no = data.emp_no

        employee.login_id = data.login_id

        employee.password = data.password

        employee.emp_name = data.emp_name

        employee.dept_cd = data.dept_cd

        employee.position_cd = data.position_cd

        employee.duty_cd = data.duty_cd

        employee.phone = data.phone

        employee.email = data.email

        employee.join_date = data.join_date

        employee.status = data.status

        employee.use_yn = "Y"

        employee.company_id = data.company_id
        employee.loc_code = data.loc_code

        EmployeeRepository.insert(
            db,
            employee
        )

        return employee

    ############################################################
    # 직원수정
    ############################################################
    @staticmethod
    def update(
            db: Session,
            emp_id: int,
            data
    ):

        employee = EmployeeRepository.get(
            db,
            emp_id
        )

        if employee is None:

            raise Exception("직원이 존재하지 않습니다.")

        
        employee.login_id = data.login_id
        employee.password = data.password
        employee.emp_name = data.emp_name
        employee.dept_cd = data.dept_cd
        employee.position_cd = data.position_cd
        employee.duty_cd = data.duty_cd

        employee.phone = data.phone

        employee.email = data.email

        employee.join_date = data.join_date

        employee.status = data.status
        employee.use_yn = data.use_yn

        employee.company_id = data.company_id
        employee.loc_code = data.loc_code

        # 비밀번호 입력 시만 변경
        #if data.password:

        #    employee.password = pwd_context.hash(
        #        data.password
        #    )

        EmployeeRepository.update(db)

        return employee

    ############################################################
    # 직원삭제
    ############################################################
    @staticmethod
    def delete(
            db: Session,
            emp_id: int
    ):

        result = EmployeeRepository.delete(
            db,
            emp_id
        )

        if not result:

            raise Exception("삭제할 직원이 없습니다.")

        return True
    
    ############################################################
    # 로그인 아이디 중복 체크
    ############################################################
    @staticmethod
    def check(
            db: Session,
            login_id: str
    ):

        row = EmployeeRepository.get(
            db,
            login_id
        )

        if row is None:

            return None

        return {
            "emp_id": row.emp_id,
            "emp_no": row.emp_no,
            "login_id": row.login_id,
            "emp_name": row.emp_name,
            "dept_cd": row.dept_cd,
            "position_cd": row.position_cd,
            "duty_cd": row.duty_cd,
            "phone": row.phone,
            "email": row.email,
            "join_date":
                row.join_date.strftime("%Y-%m-%d")
                if row.join_date else "",
            "status": row.status,
            "use_yn": row.use_yn,
            "company_id": row.company_id,
            "loc_code": row.loc_code
        }