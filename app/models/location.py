from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from app.database import Base


class Location(Base):

    __tablename__ = "TB_COMPANY_LOCATION"

    company_id = Column(
        "COMPANY_ID",
        String(50),
        primary_key=True
    )
    company_name = Column(
        "COMPANY_NAME",
        String(100),
        nullable=False
    )
    loc_code = Column(
        "LOC_CODE",
        String(50),
        primary_key=True
    )
    lat = Column(
        "lat",
        Float,
        nullable=False
    )
    lng = Column(
        "lng",
        Float,
        nullable=False
    )
    accuracy = Column(
        "accuracy",
        Float,
        nullable=False
    )
    remark = Column(
        "REMARK",
        String(200),
        nullable=False
    )
    use_yn = Column(
        "USE_YN",
        String(1),
        nullable=False,
        default="Y"
    )
    reg_date = Column(
        "REG_DATE",
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )