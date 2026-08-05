from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.department import Department
from app.models.employee import Employee

class DepartmentTreeRepository:

    ############################################################
    # 부서목록
    ############################################################
    @staticmethod
    def list(
            db: Session,
            dept_name: str = "",
            sort_no=None,
            use_yn: str = "",
            dept_cd: str = ""
    ):

        query = (
            db.query(
                Department,
                func.count(Employee.emp_id).label("emp_count")
            )
            .outerjoin(
                Employee,
                Department.dept_cd == Employee.dept_cd
            )
        )

        if dept_cd:
            query = query.filter(
                Department.dept_cd == dept_cd
            )

        if dept_name:
            query = query.filter(
                Department.dept_name.contains(dept_name)
            )

        if sort_no not in ("", None):
            query = query.filter(
                Department.sort_no == int(sort_no)
            )

        if use_yn:
            query = query.filter(
                Department.use_yn == use_yn
            )

        rows = (
            query
            .group_by(
                Department.dept_cd,
                Department.dept_name,
                Department.parent_cd,
                Department.sort_no,
                Department.use_yn,
                Department.remark,
                Department.reg_date,
                Department.upd_date
            )
            .order_by(
                Department.sort_no,
                Department.dept_cd
            )
            .all()
        )

        return rows

    ############################################################
    # Tree 조회
    ############################################################
    @staticmethod
    def tree(db: Session):

        rows = (
            db.query(Department)
            .order_by(
                Department.sort_no,
                Department.dept_cd
            )
            .all()
        )

        return rows

    ############################################################
    # 부서조회
    ############################################################
    @staticmethod
    def get(
            db: Session,
            dept_cd: str
    ):

        return (
            db.query(Department)
            .filter(
                Department.dept_cd == dept_cd
            )
            .first()
        )

    ############################################################
    # 등록
    ############################################################
    @staticmethod
    def insert(
            db: Session,
            department
    ):

        db.add(department)
        db.commit()
        db.refresh(department)

        return department

    ############################################################
    # 수정
    ############################################################
    @staticmethod
    def update(db: Session):

        db.commit()

    ############################################################
    # 삭제
    ############################################################
    @staticmethod
    def delete(
            db: Session,
            dept_cd: str
    ):

        row = (
            db.query(Department)
            .filter(
                Department.dept_cd == dept_cd
            )
            .first()
        )

        if row:

            db.delete(row)
            db.commit()

            return True

        return False

    ############################################################
    # 사용여부 변경
    ############################################################
    @staticmethod
    def update_use_yn(
            db: Session,
            dept_cd: str,
            use_yn: str
    ):

        row = (
            db.query(Department)
            .filter(
                Department.dept_cd == dept_cd
            )
            .first()
        )

        if row is None:
            return False

        row.use_yn = use_yn

        db.commit()

        return True