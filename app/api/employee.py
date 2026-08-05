from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.employee_service import EmployeeService
from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate
)

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


###################################################
# 직원목록
###################################################
@router.get("/list")
def employee_list(
    emp_no: str = "",
    emp_name: str = "",
    dept_cd: str = "",
    status: str = "",
    db: Session = Depends(get_db)
):

    return EmployeeService.list(
        db,
        emp_no,
        emp_name,
        dept_cd,
        status
    )


###################################################
# 직원상세
###################################################
@router.get("/{emp_id}")
def employee_get(
    emp_id: int,
    db: Session = Depends(get_db)
):
    row = EmployeeService.get(
        db,
        emp_id
    )
    if row is None:
        raise HTTPException(
            status_code=404,
            detail="직원을 찾을 수 없습니다."
        )
    return row


###################################################
# 직원등록
###################################################
@router.post("")
def employee_create(
    dto: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        EmployeeService.create(
            db,
            dto
        )
        return {
            "result":"OK"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


###################################################
# 직원수정
###################################################
@router.put("/{emp_id}")
def employee_update(
    emp_id:int,
    dto:EmployeeUpdate,
    db:Session=Depends(get_db)
):
    try:
        EmployeeService.update(
            db,
            emp_id,
            dto
        )
        return {
            "result":"OK"
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


###################################################
# 직원삭제
###################################################
@router.delete("/{emp_id}")
def employee_delete(
    emp_id:int,
    db:Session=Depends(get_db)
):
    EmployeeService.delete(
        db,
        emp_id
    )
    return {
        "result":"OK"
    }

#########################################################
# 사번 중복체크
#########################################################
@router.get("/check/{emp_no}")

def exists(

    emp_no: str,

    db: Session = Depends(get_db)

):

    return {

        "exists":

        EmployeeService.exists(

            db,

            emp_no

        )

    }