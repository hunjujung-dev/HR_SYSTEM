from pydantic import BaseModel
from typing import List, Dict, Any

class DashboardResponse(BaseModel):
    employee_count: int
    checkin_count: int
    checkout_count: int
    pending_device: int
    gps_company: int
    today_work: int

    notice: List[Dict[str, Any]]
    recent_checkin: List[Dict[str, Any]]

    attendance_chart: Dict[str, Any]
    dept_chart: Dict[str, Any]