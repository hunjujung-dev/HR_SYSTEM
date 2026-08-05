from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import NVARCHAR

from sqlalchemy.sql import func

from app.database import Base


class Department(Base):

    __tablename__ = "TB_DEPARTMENT"

    dept_cd = Column(
        "DEPT_CD",
        String(20),
        primary_key=True
    )

    dept_name = Column(
        "DEPT_NAME",
        NVARCHAR(100),
        nullable=False
    )

    parent_cd = Column(
        "PARENT_CD",
        String(20)
    )

    sort_no = Column(
        "SORT_NO",
        Integer,
        default=0
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