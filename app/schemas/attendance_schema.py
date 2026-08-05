from pydantic import BaseModel

############################################################
# 출근 기록 요청
############################################################
class AttendanceInRequest(BaseModel):
    emp_id: int | None = None
    user_id: str | None = None
    work_date: str | None = None
    in_time: str | None = None
    out_time: str | None = None
    in_lat: float | None = None
    in_lng: float | None = None
    out_lat: float | None = None
    out_lng: float | None = None
    status: str | None = None


############################################################
# 퇴근 기록 요청
############################################################
class AttendanceOutRequest(BaseModel):
    user_id: str | None = None
    out_time: str | None = None
    out_lat: float | None = None
    out_lng: float | None = None
    status: str | None = None
    device_id: str | None = None
    lat: float | None = None
    lng: float | None = None
    accuracy: float | None = None