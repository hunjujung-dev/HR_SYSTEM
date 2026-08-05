from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


############################################################
# 부서 등록
############################################################
class DepartmentCreate(BaseModel):

    dept_cd: str
    dept_name: str
    parent_cd: str

    sort_no: int = 0

    use_yn: str = "Y"


############################################################
# 부서 수정
############################################################
class DepartmentUpdate(BaseModel):

    dept_name: str
    parent_cd: str

    sort_no: int = 0

    use_yn: str = "Y"


############################################################
# 부서 조회
############################################################
class DepartmentResponse(BaseModel):

    dept_cd: str
    dept_name: str
    parent_cd: str

    sort_no: int = 0

    use_yn: str = "Y"