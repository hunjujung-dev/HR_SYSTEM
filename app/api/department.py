from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.department_service import DepartmentService
from app.schemas.department_schema import (
    DepartmentCreate,
    DepartmentUpdate
)

router = APIRouter(
    prefix="/department",
    tags=["Department"]
)

###################################################
# Tree
###################################################
@router.get("/tree")
def department_tree(
    db: Session = Depends(get_db)
    ):
    return DepartmentService.tree(db)

###################################################
# 부서목록
###################################################
@router.get("/list")
def department_list(
    dept_name: str = "",
    sort_no: str = "",
    use_yn: str = "",

    db: Session = Depends(get_db)
):

    return DepartmentService.list(
        db,
        dept_name,
        sort_no,
        use_yn
    )

###################################################
# 부서상세
###################################################
@router.get("/{dept_cd}")
def department_get(
    dept_cd: str,
    db: Session = Depends(get_db)
):
    row = DepartmentService.get(
        db,
        dept_cd
    )

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="부서를 찾을 수 없습니다."
        )
    return row


###################################################
# 부서등록
###################################################
@router.post("")
def department_create(

    dto: DepartmentCreate,

    db: Session = Depends(get_db)

):

    try:
        DepartmentService.create(
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
# 부서수정
###################################################
@router.put("/{dept_cd}")
def department_update(

    dept_cd:str,

    dto:DepartmentUpdate,

    db:Session=Depends(get_db)

):

    try:

        DepartmentService.update(
            db,
            dept_cd,
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
# 부서삭제
###################################################
@router.delete("/{dept_cd}")
def department_delete(

    dept_cd:str,

    db:Session=Depends(get_db)

):

    DepartmentService.delete(
        db,
        dept_cd
    )

    return {
        "result":"OK"
    }

