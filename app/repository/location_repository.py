from sqlalchemy.orm import Session

from app.models.location import Location


class LocationRepository:

    @staticmethod
    def list(
            db: Session,
            company_name="",
            use_yn=""
    ):

        query = db.query(Location)

        if company_name:
            query = query.filter(
                Location.company_name.contains(company_name)
            )

        if use_yn:
            query = query.filter(
                Location.use_yn.contains(use_yn)
            )

        return query.order_by(
            Location.reg_date.desc()
        ).all()
        
    @staticmethod
    def get(db: Session, company_id: str, loc_code: str ):

        return db.query(Location).filter(
            Location.company_id == company_id,
            Location.loc_code == loc_code
        ).first()
    

    @staticmethod
    def insert(db: Session, location):

        db.add(location)
        db.commit()
        db.refresh(location)

        return location
    
    
    @staticmethod
    def update(db: Session, location):

        db.merge(location)
        db.commit()
        db.refresh(location)

        return location
