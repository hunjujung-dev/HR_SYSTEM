from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from app.database import Base


class Attendance(Base):
    __tablename__ = "TB_ATTENDANCE"

    id = Column(
        "id",
        Integer, 
        primary_key=True
     )
    emp_id = Column(
        "EMP_ID",
        Integer,
        nullable=False
    )
    user_id = Column(
        "USER_ID",
        String(50)
    )
    work_date = Column(
        "WORK_DATE",
        Date, 
        default=datetime.utcnow
    )
    in_time = Column(
        "IN_TIME",
        DateTime,
        default=datetime.utcnow
    )
    out_time = Column(
        "OUT_TIME",
        DateTime,
        nullable=True
    )
    in_lat = Column(
        "IN_LAT",
        Float
    )
    in_lng = Column(
        "IN_LNG",
        Float
    )
    out_lat = Column(
        "OUT_LAT",
        Float
    )
    out_lng = Column(
        "OUT_LNG",
        Float
    )
    status = Column(
        "STATUS",
        String(20),
        default="IN"
    )  # in(출근), out(퇴근), absent, late, early


class Attendance_log(Base):
    __tablename__ = "TB_ATTENDANCE_LOG"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(20))
    work_date = Column(Date)

    work_lat = Column(Float)
    work_lng = Column(Float)

    company_lat = Column(Float)
    company_lng = Column(Float)

    err_msg = Column(String(500))

    reg_date = Column(DateTime)