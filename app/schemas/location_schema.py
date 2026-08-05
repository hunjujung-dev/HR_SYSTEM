from pydantic import BaseModel

############################################################
# 회사위치 정보 등록 요청
############################################################
class LocationAddRequest(BaseModel):
    company_id: str | None = None
    company_name: str | None = None
    loc_code: str | None = None
    lat: float | None = None
    lng: float | None = None
    accuracy: float | None = None
    remark: str | None = ""
    use_yn: str | None = "Y"


############################################################
# 회사위치 정보 수정 요청
############################################################
class LocationUpdateRequest(BaseModel):

    company_name: str
    lat: float
    lng: float
    accuracy: float
    remark:str
    use_yn: str | None = "Y"