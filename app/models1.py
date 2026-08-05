from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime

from app.database import Base


class Employee(Base):

    __tablename__ = "TB_EMPLOYEE"

    emp_id = Column(Integer, primary_key=True, index=True)

    emp_no = Column(String(20), unique=True)

    emp_name = Column(String(100))

    dept_cd = Column(String(20))

    position_cd = Column(String(20))

    phone = Column(String(30))

    email = Column(String(100))

    status = Column(String(20))

    join_date = Column(Date)

    retire_date = Column(Date)

    use_yn = Column(String(1))

    reg_date = Column(DateTime)