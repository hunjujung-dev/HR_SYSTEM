from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.service.location_service import LocationService
from app.schemas.location_schema import (
    LocationAddRequest,
    LocationUpdateRequest
)

router = APIRouter(
    prefix="/location",
    tags=["Location"]
)


###################################################
# 회사위치정보 목록
###################################################
@router.get("/list")
def location_list(
    company_name: str = "",
    use_yn: str = "",
    db: Session = Depends(get_db)
):

    return LocationService.list(
        db,
        company_name=company_name,
        use_yn=use_yn
    )

###################################################
# 회사위치정보 등록
###################################################
@router.post("")
def location_create(

    dto: LocationAddRequest,

    db: Session = Depends(get_db)

):

    try:
        result = LocationService.create(
            db,
            dto.company_id,
            dto.company_name,
            dto.loc_code,
            dto.lat,
            dto.lng,
            dto.accuracy,
            dto.remark,
            dto.use_yn
        )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        ) from e
    
###################################################
# 회사위치정보 상세조회
###################################################
@router.get("/{company_id}/{loc_code}")
def location_detail(
    company_id: str,
    loc_code: str,
    db: Session = Depends(get_db)
):
    location = LocationService.get(db, company_id, loc_code)
    if not location:
        raise HTTPException(status_code=404, detail="회사 위치를 찾을 수 없습니다.")
    return {
        "company_id": location.company_id,
        "company_name": location.company_name,
        "loc_code": location.loc_code,
        "lat": location.lat,
        "lng": location.lng,
        "accuracy": location.accuracy,
        "remark": location.remark,
        "use_yn": location.use_yn,
        "reg_date": location.reg_date,
    }


###################################################
# 회사위치정보 수정
###################################################
@router.put("/{company_id}/{loc_code}")
def location_update(

    company_id: str,
    loc_code: str,

    dto: LocationUpdateRequest,

    db: Session = Depends(get_db)

):

    try:

        LocationService.update(
            db,
            company_id,
            loc_code,
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