from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.device_service import DeviceService
from app.schemas.device_schema import (
    DeviceAddRequest,
    DeviceApproveRequest,
    DeviceRejectRequest
)

router = APIRouter(
    prefix="/device",
    tags=["Device"]
)


###################################################
# 디바이스 목록
###################################################
@router.get("/list")
def device_list(
    login_id: str = "",
    device_id: str = "",
    device_name: str = "",
    status: str = "",
    db: Session = Depends(get_db)
):

    return DeviceService.list(
        db,
        device_name=device_name,
        login_id=login_id,
        status=status
    )

###################################################
# 디바이스 요청 등록
###################################################
@router.post("")
def device_create(

    dto: DeviceAddRequest,

    db: Session = Depends(get_db)

):

    try:
        result = DeviceService.create(
            db,
            dto.login_id,
            dto.device_id,
            dto.device_name
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
###################################################
# 디바이스 승인처리
###################################################
@router.post("/approve")
def device_approve(

    dto: DeviceApproveRequest,

    db: Session = Depends(get_db)
):

    try:
        result = DeviceService.approve(
            db,
            dto.device_id
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    db: Session = Depends(get_db)


###################################################
# 디바이스 거부처리
###################################################
@router.post("/reject")
def device_reject(

    dto: DeviceRejectRequest,

    db: Session = Depends(get_db)
):

    try:
        result = DeviceService.reject(
            db,
            dto.device_id
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
