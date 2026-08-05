from pydantic import BaseModel

############################################################
# 디바이스 등록 요청
############################################################
class DeviceAddRequest(BaseModel):
    login_id: str
    device_id: str
    device_name: str


############################################################
# 요청디바이스 승인/거부
############################################################
class DeviceApproveRequest(BaseModel):
    login_id: str | None = None
    device_id: str

class DeviceRejectRequest(BaseModel):
    login_id: str | None = None
    device_id: str