from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.department_service_tree import DepartmentTreeService
from app.schemas.department_schema import (
    DepartmentCreate,
    DepartmentUpdate
)

router = APIRouter(
    prefix="/departmenttree",
    tags=["DepartmentTree"]
)

############################################################
# 부서목록
############################################################
@router.get("/list")
def departmenttee_list(
    dept_name: str = "",
    sort_no: str = "",
    use_yn: str = "",
    dept_cd: str = "",
    db: Session = Depends(get_db)
):

    return DepartmentTreeService.list(
        db=db,
        dept_name=dept_name,
        sort_no=sort_no,
        use_yn=use_yn,
        dept_cd=dept_cd
    )


############################################################
# Tree
############################################################
@router.get("/tree")
def department_tree(
    db: Session = Depends(get_db)
):

    return DepartmentTreeService.tree(db)


############################################################
# 부서조회
############################################################
@router.get("/{dept_cd}")
def departmenttree_get(
    dept_cd: str,
    db: Session = Depends(get_db)
):

    row = DepartmentTreeService.get(
        db,
        dept_cd
    )

    if row is None:

        raise HTTPException(
            status_code=404,
            detail="부서를 찾을 수 없습니다."
        )

    return row


############################################################
# 등록
############################################################
@router.post("")
def departmenttree_create(
    dto: DepartmentCreate,
    db: Session = Depends(get_db)
):
    try:
        DepartmentTreeService.create(
            db,
            dto
        )

        return {
            "result": "OK"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


############################################################
# 수정
############################################################
@router.put("/{dept_cd}")
def departmenttree_update(
    dept_cd: str,
    dto: DepartmentUpdate,
    db: Session = Depends(get_db)
):
    try:
        DepartmentTreeService.update(
            db,
            dept_cd,
            dto
        )

        return {
            "result": "OK"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


############################################################
# 삭제
############################################################
@router.delete("/{dept_cd}")
def departmenttree_delete(
    dept_cd: str,
    db: Session = Depends(get_db)
):
    try:
        DepartmentTreeService.delete(
            db,
            dept_cd
        )

        return {
            "result": "OK"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


############################################################
# 사용여부 변경 (Ajax)
############################################################
@router.put("/useyn/{dept_cd}")
def change_useyn(
    dept_cd: str,
    use_yn: str,
    db: Session = Depends(get_db)
):

    try:

        DepartmentTreeService.change_use_yn(
            db,
            dept_cd,
            use_yn
        )

        return {
            "result": "OK"
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


############################################################
# Drag & Drop Sort 저장
############################################################
@router.put("/sort")
def save_sort(
    items: list,
    db: Session = Depends(get_db)
):
    try:
        DepartmentTreeService.save_sort(
            db,
            items
        )

        return {
            "result": "OK"
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )