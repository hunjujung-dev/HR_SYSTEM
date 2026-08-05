from sqlalchemy.orm import Session

from app.models.device import Device


class DeviceRepository:

    @staticmethod
    def list(
            db: Session,
            device_name="",
            user_id="",
            status=""
    ):

        query = db.query(Device)

        if device_name:
            query = query.filter(
                Device.device_name.contains(device_name)
            )

        if user_id:
            query = query.filter(
                Device.user_id.contains(user_id)
            )

        if status:
            query = query.filter(
                Device.status.contains(status)
            )

        return query.order_by(
            Device.reg_date.desc()
        ).all()
        
    @staticmethod
    def get(db: Session, emp_id):

        return db.query(Device).filter(
            Device.emp_id == emp_id
        ).first()
    

    @staticmethod
    def insert(db: Session, device):

        db.add(device)
        db.commit()
        db.refresh(device)

        return device
    
    
    @staticmethod
    def update(db: Session, device):

        db.merge(device)
        db.commit()
        db.refresh(device)

        return device
