from pydantic import BaseModel
from typing import Optional


class EmployeeSearch(BaseModel):

    emp_no: Optional[str] = ""

    emp_name: Optional[str] = ""

    dept_cd: Optional[str] = ""

    status: Optional[str] = ""


class EmployeeSave(BaseModel):

    emp_id: int | None = None

    emp_no: str

    emp_name: str

    dept_cd: str

    position_cd: str

    phone: str

    email: str

    status: str