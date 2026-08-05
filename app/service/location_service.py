from datetime import datetime

from sqlalchemy.orm import Session

from app.models.location import Location
from app.repository.location_repository import LocationRepository


class LocationService:

    ############################################################
    # 위치정보목록
    ############################################################
    @staticmethod
    def list(db: Session,
            company_name="",
            use_yn=""):

        rows = LocationRepository.list(
            db,
            company_name,
            use_yn
        )

        result = []

        for row in rows:

            result.append({
                "company_id": row.company_id,
                "company_name": row.company_name,
                "loc_code": row.loc_code,
                "lat": row.lat,
                "lng": row.lng,
                "accuracy": row.accuracy,
                "remark": row.remark,
                "use_yn": row.use_yn,
                "reg_date": row.reg_date
            })

        return result
    
    ############################################################
    # 회사 위치정보 요청
    ############################################################
    @staticmethod
    def create(
        db,
        company_id,
        company_name,
        loc_code,
        lat,
        lng,
        accuracy,
        remark,
        use_yn
    ):

        if company_id is None:
            company_id = ""
        if company_name is None:
            company_name = ""
        if loc_code is None:
            loc_code = ""
        if lat is None:
            lat = 0
        if lng is None:
            lng = 0
        if accuracy is None:
            accuracy = 0
        if remark is None:
            remark = ""
        if use_yn is None:
            use_yn = "Y"

        location = db.query(Location).filter(
            Location.company_id == company_id,
            Location.loc_code == loc_code
        ).first()

        if location:
            return {
                "result":"FAIL",
                "msg":"이미 등록된 위치정보"
            }

        new_location = Location(
            company_id=company_id,
            company_name=company_name,
            loc_code=loc_code,
            lat=lat,
            lng=lng,
            accuracy=accuracy,
            remark=remark,
            use_yn=use_yn,
            reg_date=datetime.utcnow()
        )

        try:
            db.add(new_location)
            db.commit()
            db.refresh(new_location)
        except Exception as exc:
            db.rollback()
            raise RuntimeError(f"위치정보 저장 실패: {exc}") from exc

        return {
            "result":"OK",
            "msg":"위치정보 등록 완료"
        }


    @staticmethod
    def get(db: Session, company_id: str, loc_code: str):
        return db.query(Location).filter(Location.company_id == company_id, Location.loc_code == loc_code).first()

    ############################################################
    # 회사 위치 수정
    ############################################################
    def update(
        db: Session,
        company_id: str,
        loc_code: str,
        dto
    ):

        location = db.query(Location).filter(
            Location.company_id == company_id,
            Location.loc_code == loc_code
        ).first()

        if not location:
            return {"result": "FAIL", "msg": "없음"}
        
        location.company_name = dto.company_name
        location.lat = dto.lat
        location.lng = dto.lng
        location.accuracy = dto.accuracy
        location.remark = dto.remark
        location.use_yn = dto.use_yn

        LocationRepository.update(db, location)

        return location