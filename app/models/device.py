from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from sqlalchemy.sql import func

from app.database import Base


class Device(Base):

    __tablename__ = "TB_DEVICE"

    device_id = Column(
        "DEVICE_ID",
        String(100),
        primary_key=True
    )
    emp_id = Column(
        "EMP_ID",
        Integer,
        nullable=False
    )
    user_id = Column(
        "LOGIN_ID",
        String(20),
        nullable=False,
        unique=True
    )

    device_name = Column(
        "DEVICE_NAME",
        String(200)
    )
    # A : ANDROID / I : IOS / W : WEB
    device_type = Column(
        "DEVICE_TYPE",
        String(30)
    )
    phone_hash = Column(
        "PHONE_HASH",
        String(50)
    )

    # PENDING / APPROVED / BLOCKED
    status = Column(
        "STATUS",
        String(20),
        nullable=False,
        default="PENDING"
    )
    
    reg_date = Column(
        "REG_DATE",
        DateTime,
        default=func.now()
    )
    approved_date = Column(
        "APPROVED_DATE",
        DateTime
    )