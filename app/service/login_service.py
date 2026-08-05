from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db as get_db_session
from app.models.employee import Employee
from app.security import create_token

router = APIRouter(prefix="", tags=["Auth"])


@router.post("/login")
def login(
    user_id: str,
    password: str,
    db: Session = Depends(get_db_session)
):
    emp = db.query(Employee).filter(
        Employee.login_id == user_id,
    ).first()

    if not emp:
        return {
            "result": "FAIL",
            "msg": "사원없음"
        }

    if emp.password != password:
        return {
            "result": "FAIL",
            "msg": "비밀번호 불일치"
        }

    token = create_token(user_id, emp.emp_id)

    return {
        "result": "OK",
        "token": token,
        "user_id": user_id + "(" + str(emp.emp_id) + ")",
        "emp_name": emp.emp_name,
        "name": emp.emp_name,
    }