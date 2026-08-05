from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.attendance_service import AttendanceService
from app.schemas.attendance_schema import (
    AttendanceInRequest,
    AttendanceOutRequest
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.get("/list")
def attendance_list(
    login_id: str = Query(default=""),
    work_date: str = Query(default=""),
    status: str = Query(default=""),
    db: Session = Depends(get_db)
):
    try:
        return AttendanceService.list(
            db,
            login_id=login_id,
            work_date=work_date,
            status=status
        )
    except Exception as exc:
        return JSONResponse(status_code=400, content={"result": "FAIL", "msg": str(exc)})


@router.post("/checkin")
def attendance_checkin(
    dto: AttendanceInRequest,
    db: Session = Depends(get_db)
):
    try:
        login_id = getattr(dto, "user_id", None) or getattr(dto, "login_id", None)
        if not login_id:
            return JSONResponse(status_code=400, content={"result": "FAIL", "msg": "로그인 아이디가 필요합니다."})

        result = AttendanceService.create(
            db,
            getattr(dto, "emp_id", 0) or 0,
            login_id,
            dto.work_date or datetime.today().date().strftime("%Y-%m-%d"),
            dto.in_time or datetime.now().strftime("%H:%M:%S"),
            getattr(dto, "out_time", None),
            getattr(dto, "in_lat", None),
            getattr(dto, "in_lng", None),
            getattr(dto, "out_lat", None),
            getattr(dto, "out_lng", None),
            dto.status or "IN"
        )
        if isinstance(result, dict) and result.get("result") == "FAIL":
            return JSONResponse(status_code=400, content=result)
        return result
    except Exception as exc:
        return JSONResponse(status_code=400, content={"result": "FAIL", "msg": str(exc)})


@router.post("/checkout")
def attendance_checkout(
    dto: AttendanceOutRequest,
    db: Session = Depends(get_db)
):
    try:
        user_id = dto.user_id or ""
        out_lat = dto.out_lat if dto.out_lat is not None else dto.lat
        out_lng = dto.out_lng if dto.out_lng is not None else dto.lng

        if not user_id:
            return JSONResponse(status_code=400, content={"result": "FAIL", "msg": "로그인 아이디가 필요합니다."})

        return AttendanceService.update(
            db,
            user_id,
            out_lat,
            out_lng
        )
    except Exception as exc:
        return JSONResponse(status_code=400, content={"result": "FAIL", "msg": str(exc)})
