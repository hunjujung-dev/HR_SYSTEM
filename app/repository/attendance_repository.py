from sqlalchemy.orm import Session

from app.models.attendance import Attendance


class AttendanceRepository:

    @staticmethod
    def repro_attendance(db: Session):
        from app.service.attendance_service import AttendanceService

        return AttendanceService.create(
            db,
            0,
            "34333",
            "2026-08-02",
            "09:00:00",
            None,
            37.5,
            127.0,
            None,
            None,
            "IN"
        )

    @staticmethod
    def list(
            db: Session,
            user_id="",
            work_date="",
            status=""
    ):

        query = db.query(Attendance)

        if work_date:
            query = query.filter(
                Attendance.work_date == work_date
            )

        if user_id:
            query = query.filter(
                Attendance.user_id == user_id
            )

        if status:
            query = query.filter(
                Attendance.status.contains(status)
            )

        return query.order_by(
            Attendance.work_date.desc(),
            Attendance.in_time.desc()
        ).all()
        
    @staticmethod
    def get(db: Session, emp_id):

        return db.query(Attendance).filter(
            Attendance.emp_id == emp_id
        ).first()
    

    @staticmethod
    def insert(db: Session, attendance):

        db.add(attendance)
        db.commit()
        db.refresh(attendance)

        return attendance


    @staticmethod
    def update(db: Session, attendance):

        db.merge(attendance)
        db.commit()
        db.refresh(attendance)

        return attendance
