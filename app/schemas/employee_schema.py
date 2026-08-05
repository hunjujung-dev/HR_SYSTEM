from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


############################################################
# 직원 등록
############################################################
class EmployeeCreate(BaseModel):

    emp_no: str
    login_id: str
    password: str

    emp_name: str

    dept_cd: str

    position_cd: str

    duty_cd: Optional[str] = None

    phone: Optional[str] = ""

    email: Optional[str] = ""

    join_date: date

    status: str = "ACTIVE"

    use_yn: str = "Y"

    company_id: Optional[str] = None
    loc_code: Optional[str] = None


############################################################
# 직원 수정
############################################################
class EmployeeUpdate(BaseModel):

    login_id: str
    password: Optional[str] = None
    emp_name: str

    dept_cd: str

    position_cd: str

    duty_cd: Optional[str] = None

    phone: Optional[str] = ""

    email: Optional[str] = ""

    join_date:  Optional[date] = None

    status: str

    use_yn: str

    company_id: Optional[str] = None
    loc_code: Optional[str] = None


############################################################
# 직원 조회
############################################################
class EmployeeResponse(BaseModel):

    emp_id: int

    emp_no: str

    login_id: str

    emp_name: str

    dept_cd: str

    position_cd: str

    duty_cd: Optional[str] = None

    phone: Optional[str] = ""

    email: Optional[str] = ""

    join_date: Optional[date] = None

    status: str

    use_yn: str

    company_id: Optional[str] = None
    loc_code: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)