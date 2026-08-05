from typing import Optional

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.employee_schema import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeSearch
)

from app.service.employee_service import EmployeeService


router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


###########################################################
# 사원 목록조회
###########################################################
@router.get("/list")
def get_list(
    page: int = 1,
    size: int = 20,
    emp_no: Optional[str] = None,
    emp_name: Optional[str] = None,
    dept_cd: Optional[str] = None,
    position_cd: Optional[str] = None,
    status: Optional[str] = None,
    use_yn: Optional[str] = None,
    db: Session = Depends(get_db)
):

    cond = EmployeeSearch(
        page=page,
        size=size,
        emp_no=emp_no,
        emp_name=emp_name,
        dept_cd=dept_cd,
        position_cd=position_cd,
        status=status,
        use_yn=use_yn
    )

    return EmployeeService.search(
        db,
        cond
    )


###########################################################
# 사원조회
###########################################################
@router.get("/{emp_no}")
def get_employee(
    emp_no: str,
    db: Session = Depends(get_db)
):

    return EmployeeService.get(
        db,
        emp_no
    )


###########################################################
# 등록
###########################################################
@router.post("")
def create(
    dto: EmployeeCreate,
    db: Session =Depends(get_db)
):

    return EmployeeService.create(
        db,
        dto
    )


###########################################################
# 수정
###########################################################
@router.put("/{emp_no}")
def update(
    emp_no:str,
    dto:EmployeeUpdate,
    db:Session=Depends(get_db)
):

    return EmployeeService.update(
        db,
        emp_no,
        dto
    )


###########################################################
# 삭제
###########################################################
@router.delete("/{emp_no}")
def delete(
    emp_no:str,
    db:Session=Depends(get_db)
):

    return EmployeeService.delete(
        db,
        emp_no
    )


###########################################################
# 사번 중복확인
###########################################################
@router.get("/exists/{emp_no}")
def exists(
    emp_no:str,
    db:Session=Depends(get_db)
):

    return {

        "exists":

        EmployeeService.exists(
            db,
            emp_no
        )

    }


###########################################################
# 사진업로드
###########################################################
@router.post("/photo/{emp_no}")
def upload_photo(

    emp_no:str,

    file:UploadFile=File(...),

    db:Session=Depends(get_db)

):

    return EmployeeService.upload_photo(

        db,

        emp_no,

        file

    )


###########################################################
# Excel Upload
###########################################################
@router.post("/excel/upload")
def excel_upload(

    rows:list,

    db:Session=Depends(get_db)

):

    return EmployeeService.excel_upload(

        db,

        rows

    )


###########################################################
# Excel Download
###########################################################
@router.get("/excel/download")
def excel_download(

    db:Session=Depends(get_db)

):

    workbook = EmployeeService.excel_download(db)

    stream = workbook.save_to_stream()

    return StreamingResponse(

        stream,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={

            "Content-Disposition":
            "attachment; filename=employee.xlsx"

        }

    )


###########################################################
# Excel Template
###########################################################
@router.get("/excel/template")
def template(

    db:Session=Depends(get_db)

):

    workbook = EmployeeService.template_download()

    stream = workbook.save_to_stream()

    return StreamingResponse(

        stream,

        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        headers={

            "Content-Disposition":
            "attachment; filename=employee_template.xlsx"

        }

    )


###########################################################
# 재직여부 변경
###########################################################
@router.put("/status/{emp_no}")
def change_status(

    emp_no:str,

    status:str,

    db:Session=Depends(get_db)

):

    return EmployeeService.change_status(

        db,

        emp_no,

        status

    )


###########################################################
# 사용여부 변경
###########################################################
@router.put("/use/{emp_no}")
def change_use(

    emp_no:str,

    use_yn:str,

    db:Session=Depends(get_db)

):

    return EmployeeService.change_use(

        db,

        emp_no,

        use_yn

    )