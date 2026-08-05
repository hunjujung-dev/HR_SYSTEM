from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from sqlalchemy.sql import func

from app.database import Base


class Employee(Base):

    __tablename__ = "TB_EMPLOYEE"

    emp_id = Column(
        "EMP_ID",
        Integer,
        primary_key=True,
        autoincrement=True
    )

    emp_no = Column(
        "EMP_NO",
        String(20),
        nullable=False,
        unique=True
    )

    login_id = Column(
        "LOGIN_ID",
        String(50),
        nullable=False,
        unique=True
    )

    password = Column(
        "PASSWORD",
        String(255),
        nullable=False
    )

    emp_name = Column(
        "EMP_NAME",
        NVARCHAR(100),
        nullable=False
    )

    dept_cd = Column(
        "DEPT_CD",
        String(20)
    )

    position_cd = Column(
        "POSITION_CD",
        String(20)
    )

    duty_cd = Column(
        "DUTY_CD",
        String(20)
    )

    phone = Column(
        "PHONE",
        String(30)
    )

    email = Column(
        "EMAIL",
        String(100)
    )

    join_date = Column(
        "JOIN_DATE",
        Date
    )

    retire_date = Column(
        "RETIRE_DATE",
        Date
    )

    status = Column(
        "STATUS",
        String(20),
        default="ACTIVE"
    )

    company_id = Column(
        "COMPANY_ID",
        String(50)
    )

    loc_code = Column(
        "LOC_CODE",
        String(50)
    )

    remark = Column(
        "REMARK",
        NVARCHAR(500)
    )

    use_yn = Column(
        "USE_YN",
        String(1),
        default="Y"
    )

    reg_date = Column(
        "REG_DATE",
        DateTime,
        default=func.now()
    )

    upd_date = Column(
        "UPD_DATE",
        DateTime,
        onupdate=func.now()
    )