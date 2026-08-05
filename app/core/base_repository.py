from sqlalchemy.orm import Session


class BaseRepository:

    model = None

    @classmethod
    def list(cls, db: Session):

        return db.query(cls.model).all()

    @classmethod
    def get(cls, db: Session, pk):

        return db.get(cls.model, pk)

    @classmethod
    def insert(cls, db: Session, obj):

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    @classmethod
    def update(cls, db: Session):

        db.commit()

    @classmethod
    def delete(cls, db: Session, pk):

        row = db.get(cls.model, pk)

        if row:

            db.delete(row)

            db.commit()

            return True

        return False

    @classmethod
    def exists(cls, db: Session, pk):

        return db.get(cls.model, pk) is not None

    @classmethod
    def count(cls, db: Session):

        return db.query(cls.model).count()