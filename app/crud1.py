from sqlalchemy.orm import Session
from app.models.employee import Employee


def employee_list(
    db: Session,
    emp_no="",
    emp_name="",
    dept_cd="",
    status=""
):

    query = db.query(Employee)

    if emp_no:
        query = query.filter(Employee.emp_no.contains(emp_no))

    if emp_name:
        query = query.filter(Employee.emp_name.contains(emp_name))

    if dept_cd:
        query = query.filter(Employee.dept_cd == dept_cd)

    if status:
        query = query.filter(Employee.status == status)

    return query.order_by(Employee.emp_no).all()