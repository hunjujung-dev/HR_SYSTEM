from sqlalchemy.orm import Session

from app.models.department import Department


class DepartmentRepository:

    @staticmethod
    def list(
            db: Session,
            dept_name="",
            sort_no=None,
            use_yn=""
    ):
        query = db.query(Department)

        if dept_name:
            query = query.filter(
                Department.dept_name.contains(dept_name)
            )

        if sort_no not in (None, ""):
            query = query.filter(
                Department.sort_no == int(sort_no)
            )

        if use_yn:
            query = query.filter(
                Department.use_yn == use_yn
            )

        return query.order_by(
            Department.dept_cd
        ).all()
    
    @staticmethod
    def tree(db: Session):
        rows = db.query(
            Department
        ).order_by(
            Department.sort_no,
            Department.dept_cd
        ).all()

        return rows


    @staticmethod
    def get(
        db: Session,
        dept_cd: str
    ):

        return db.query(
            Department
        ).filter(
            Department.dept_cd == dept_cd
        ).first()


    @staticmethod
    def insert(
        db: Session,
        department
    ):

        db.add(department)

        db.commit()

        db.refresh(department)

        return department


    @staticmethod
    def update(db):

        db.commit()
        return True


    @staticmethod
    def delete(
        db,
        dept_cd
    ):

        row = db.query(
            Department
        ).filter(
            Department.dept_cd == dept_cd
        ).first()

        if row:

            db.delete(row)

            db.commit()

            return True

        return False