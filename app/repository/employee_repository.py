from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.employee import Employee


class EmployeeRepository:

    @staticmethod
    def list(
            db: Session,
            emp_no="",
            emp_name="",
            dept_cd="",
            status=""
    ):

        query = db.query(Employee)

        if emp_no:
            query = query.filter(
                Employee.emp_no.contains(emp_no)
            )

        if emp_name:
            query = query.filter(
                Employee.emp_name.contains(emp_name)
            )

        if dept_cd:
            query = query.filter(
                Employee.dept_cd == dept_cd
            )

        if status:
            query = query.filter(
                Employee.status == status
            )

        return query.order_by(
            Employee.emp_no
        ).all()


    @staticmethod
    def get(db: Session, emp_id):

        return db.query(Employee).filter(
            Employee.emp_id == emp_id
        ).first()


    @staticmethod
    def insert(db: Session, employee):

        db.add(employee)

        db.commit()

        db.refresh(employee)

        return employee


    @staticmethod
    def update(db: Session):

        db.commit()


    @staticmethod
    def delete(db: Session, emp_id):

        row = db.query(Employee).filter(
            Employee.emp_id == emp_id
        ).first()

        if row:

            db.delete(row)

            db.commit()

            return True

        return False