from pydantic import BaseModel

############################################################
# 로그인
############################################################
class CheckInRequest(BaseModel):
    device_id: str
    lat: float
    lng: float
    accuracy: float


############################################################
# 로그아웃
############################################################
class CheckOutRequest(BaseModel):
    device_id: str
    lat: float
    lng: float
    accuracy: float