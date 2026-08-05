from sqlalchemy.orm import Session

from app.models.employee import Employee

class LoginRepository:

    @staticmethod
    def get(db: Session, user_id: str, password: str):

        return db.query(Employee).filter(
            Employee.user_id == user_id,
            Employee.password == password
        ).first()


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Employee
from app.security import create_token

router = APIRouter()

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/login")
def login(
    user_id:str,
    password:str,
    db:Session=Depends(get_db)
):

    emp = db.query(Employee).filter(
        #Employee.user_id == user_id
        Employee.user_id == user_id,
        Employee.password_hash == password
    ).first()

    if not emp:

        return {
            "result":"FAIL",
            "msg":"사원없음"
        }

    #token = create_token({"emp_id": emp.emp_id})
    token = create_token(user_id, emp.emp_id)

    return {
        "result":"OK",
        "token":token,
        "user_id": user_id + "(" + str(emp.emp_id) + ")",
        "emp_name": emp.emp_name,
        "name": emp.emp_name
    }