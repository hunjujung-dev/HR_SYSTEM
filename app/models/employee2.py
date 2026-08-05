from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from sqlalchemy.sql import func

from app.database import Base


class Employee(Base):

    __tablename__="TB_EMPLOYEE"


    emp_id = Column(
        Integer,
        primary_key=True
    )


    emp_no = Column(
        String(20),
        unique=True
    )


    emp_name = Column(
        String(100)
    )


    dept_cd = Column(
        String(20)
    )


    position_cd = Column(
        String(20)
    )


    duty_cd = Column(
        String(20)
    )


    login_id = Column(
        String(50)
    )


    password = Column(
        String(255)
    )


    email = Column(
        String(100)
    )


    phone = Column(
        String(20)
    )


    zip_code = Column(
        String(10)
    )


    address1 = Column(
        String(200)
    )


    address2 = Column(
        String(200)
    )


    birth_date = Column(
        Date
    )


    join_date = Column(
        Date
    )


    retire_date = Column(
        Date
    )


    status = Column(
        String(20)
    )


    device_id = Column(
        String(100)
    )


    remark = Column(
        String(500)
    )


    use_yn = Column(
        String(1)
    )


    reg_id = Column(
        String(30)
    )


    reg_date = Column(
        DateTime
    )


    upd_id = Column(
        String(30)
    )


    upd_date = Column(
        DateTime
    )