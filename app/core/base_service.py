from sqlalchemy.orm import Session

from app.core.response import Response
from app.core.exception import (
    DuplicateException,
    NotFoundException,
    ValidateException
)


class BaseService:

    repository = None

    ####################################################
    # 목록
    ####################################################
    @classmethod
    def list(cls, db: Session):

        rows = cls.repository.list(db)

        return Response.data(rows)

    ####################################################
    # 조회
    ####################################################
    @classmethod
    def get(cls, db: Session, pk):

        row = cls.repository.get(db, pk)

        if row is None:

            raise NotFoundException("데이터가 존재하지 않습니다.")

        return Response.data(row)

    ####################################################
    # 등록
    ####################################################
    @classmethod
    def create(cls, db: Session, obj):

        return cls.repository.insert(db, obj)

    ####################################################
    # 수정
    ####################################################
    @classmethod
    def update(cls, db: Session):

        cls.repository.update(db)

        return Response.ok("저장되었습니다.")

    ####################################################
    # 삭제
    ####################################################
    @classmethod
    def delete(cls, db: Session, pk):

        result = cls.repository.delete(db, pk)

        if not result:

            raise NotFoundException("삭제할 데이터가 없습니다.")

        return Response.ok("삭제되었습니다.")

    ####################################################
    # 존재 여부
    ####################################################
    @classmethod
    def exists(cls, db: Session, pk):

        return cls.repository.exists(db, pk)

    ####################################################
    # 중복검사
    ####################################################
    @classmethod
    def duplicate(cls, db: Session, pk, message="이미 존재합니다."):

        if cls.repository.exists(db, pk):

            raise DuplicateException(message)

    ####################################################
    # 필수값
    ####################################################
    @staticmethod
    def required(value, message):

        if value is None:

            raise ValidateException(message)

        if isinstance(value, str):

            if value.strip() == "":

                raise ValidateException(message)

    ####################################################
    # 최대길이
    ####################################################
    @staticmethod
    def max_length(value, length, message):

        if value is None:

            return

        if len(value) > length:

            raise ValidateException(message)

    ####################################################
    # 최소길이
    ####################################################
    @staticmethod
    def min_length(value, length, message):

        if value is None:

            return

        if len(value) < length:

            raise ValidateException(message)

    ####################################################
    # 숫자검사
    ####################################################
    @staticmethod
    def numeric(value, message):

        if value is None:

            return

        try:

            float(value)

        except Exception:

            raise ValidateException(message)

    ####################################################
    # 날짜검사
    ####################################################
    @staticmethod
    def date(value, message):

        if value is None:

            return

        import datetime

        try:

            datetime.datetime.strptime(
                value,
                "%Y-%m-%d"
            )

        except Exception:

            raise ValidateException(message)