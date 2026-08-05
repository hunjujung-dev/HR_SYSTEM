from datetime import date, datetime

from typing import Optional

from pydantic import BaseModel
from pydantic import ConfigDict


############################################################
# 등록
############################################################

class EmployeeCreate(BaseModel):
    emp_no:str
    emp_name:str
    emp_eng_name:Optional[str]=None
    dept_cd:str
    position_cd:Optional[str]=None
    duty_cd:Optional[str]=None
    phone:Optional[str]=None
    email:Optional[str]=None
    zip_code:Optional[str]=None
    address1:Optional[str]=None
    address2:Optional[str]=None
    join_date:Optional[date]=None
    retire_date:Optional[date]=None
    company_id:Optional[str]=None
    loc_code:Optional[str]=None
    status:str="WORK"
    photo:Optional[str]=None
    use_yn:str="Y"
    remark:Optional[str]=None

############################################################
# 수정
############################################################

class EmployeeUpdate(BaseModel):
    emp_name:str
    emp_eng_name:Optional[str]=None
    dept_cd:str
    position_cd:Optional[str]=None
    duty_cd:Optional[str]=None
    phone:Optional[str]=None
    email:Optional[str]=None
    zip_code:Optional[str]=None
    address1:Optional[str]=None
    address2:Optional[str]=None
    join_date:Optional[date]=None
    retire_date:Optional[date]=None
    company_id:Optional[str]=None
    loc_code:Optional[str]=None
    status:str="WORK"
    photo:Optional[str]=None
    use_yn:str="Y"
    remark:Optional[str]=None

############################################################
# 조회
############################################################

class EmployeeRequest(BaseModel):
    model_config=ConfigDict(
        from_attributes=True
    )

    emp_no:str

    emp_name:str

    emp_eng_name:Optional[str]

    dept_cd:str

    position_cd:Optional[str]

    duty_cd:Optional[str]

    phone:Optional[str]

    email:Optional[str]

    zip_code:Optional[str]

    address1:Optional[str]

    address2:Optional[str]

    join_date:Optional[date]

    retire_date:Optional[date]

    status:str

    company_id:Optional[str]=None
    loc_code:Optional[str]=None

    photo:Optional[str]

    use_yn:str

    remark:Optional[str]

    reg_date:Optional[datetime]

    upd_date:Optional[datetime]


############################################################
# 검색
############################################################

class EmployeeSearch(BaseModel):

    emp_no:Optional[str]=None

    emp_name:Optional[str]=None

    dept_cd:Optional[str]=None

    position_cd:Optional[str]=None

    status:Optional[str]=None

    use_yn:Optional[str]=None

    page:int=1

    size:int=20

##################################################
# 사원 등록 요청
##################################################

class EmployeeCreateRequest(BaseModel):
    emp_no: str
    emp_name: str
    dept_cd: str
    position_cd: str
    duty_cd: Optional[str] = None
    login_id: str
    password: str
    email: Optional[str] = None
    phone: Optional[str] = None
    zip_code: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    birth_date: Optional[date] = None
    join_date: date
    retire_date: Optional[date] = None
    company_id:Optional[str]=None
    loc_code:Optional[str]=None
    status: str = "ACTIVE"
    device_id: Optional[str] = None
    remark: Optional[str] = None



##################################################
# 수정
##################################################

class EmployeeUpdateRequest(BaseModel):
    emp_name: Optional[str] = None
    dept_cd: Optional[str] = None
    position_cd: Optional[str] = None
    duty_cd: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address1: Optional[str] = None
    address2: Optional[str] = None
    status: Optional[str] = None
    remark: Optional[str] = None
    company_id:Optional[str]=None
    loc_code:Optional[str]=None


##################################################
# Response
##################################################

class EmployeeResponse(BaseModel):
    emp_id:int
    emp_no:str
    emp_name:str
    dept_cd:str
    position_cd:str
    duty_cd:Optional[str]
    login_id:str
    email:Optional[str]
    phone:Optional[str]
    join_date:date
    company_id:Optional[str]=None
    loc_code:Optional[str]=None
    retire_date:Optional[date]
    status:str


class Config:

    from_attributes=True