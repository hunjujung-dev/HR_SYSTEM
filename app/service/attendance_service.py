from datetime import datetime
from datetime import time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.device import Device
from app.models.location import Location
from app.repository.attendance_repository import AttendanceRepository


class AttendanceService:

    ############################################################
    # 출퇴근 기록 목록
    ############################################################
    @staticmethod
    def list(db: Session,
            login_id="",
            work_date="",
            status=""):
        
        rows = AttendanceRepository.list(
            db,
            user_id=login_id,
            work_date=work_date,
            status=status
        )

        result = []

        for row in rows:
            login_id_value = getattr(row, "user_id", None)
            if login_id_value is None:
                login_id_value = getattr(row, "login_id", "")

            result.append({
                "id": row.id,
                "emp_id": row.emp_id,
                "login_id": login_id_value,
                "work_date": row.work_date,
                "in_time": row.in_time,
                "out_time": row.out_time,
                "in_lat": row.in_lat,
                "in_lng": row.in_lng,
                "out_lat": row.out_lat,
                "out_lng": row.out_lng,
                "status": row.status
            })

        return result
    
    ############################################################
    # 출근 기록 요청
    ############################################################
    @staticmethod
    def create(
        db,
        emp_id,
        login_id,
        work_date,
        in_time,
        out_time=None,
        in_lat=None,
        in_lng=None,
        out_lat=None,
        out_lng=None,
        status="IN"
    ):
        
        if login_id is None or login_id == "":
            return {"result": "FAIL", "msg": "로그인 아이디가 필요합니다."}

        employee = db.query(Employee).filter(
            Employee.login_id == login_id
        ).first()

        if not employee:
            return {"result": "FAIL", "msg": "미 등록 아이디"}
        if employee.use_yn == "N":
            return {"result": "FAIL", "msg": "사용불가 아이디"}

        resolved_emp_id = employee.emp_id

        current_dt = datetime.now()
        current_time = current_dt.strftime("%H:%M:%S")
        current_date = current_dt.date().strftime("%Y-%m-%d")

        if not in_time:
            in_time = current_time
        if not work_date:
            work_date = current_date

        if isinstance(in_time, str):
            try:
                if len(in_time) <= 8 and ":" in in_time:
                    parsed_time = datetime.strptime(in_time, "%H:%M:%S").time()
                    in_time = datetime.combine(datetime.strptime(work_date, "%Y-%m-%d").date(), parsed_time)
                else:
                    in_time = datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                try:
                    in_time = datetime.strptime(in_time, "%H:%M:%S")
                except ValueError:
                    in_time = current_dt

        new_attendance = Attendance(
            emp_id=resolved_emp_id,
            user_id=login_id,
            work_date=work_date,
            in_time=in_time,
            out_time=out_time,
            in_lat=in_lat,
            in_lng=in_lng,
            out_lat=out_lat,
            out_lng=out_lng,
            status=status
        )

        db.add(new_attendance)
        db.commit()

        return {
            "result":"OK",
            "msg":"출근 등록 완료"
        }

    
    ############################################################
    # 퇴근 기록 요청
    ############################################################
    @staticmethod
    def update(db, user_id, out_lat, out_lng):

        attendance = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.status == "IN"
        ).order_by(Attendance.id.desc()).first()

        if not attendance:
            return {"result": "FAIL", "msg": "없음"}

        attendance.status = "OUT"
        attendance.out_time = datetime.now()
        attendance.out_lat = out_lat
        attendance.out_lng = out_lng
        db.commit()

        return {"result": "OK", "msg": "퇴근 기록 완료"}
    
    @staticmethod
    def get_company_location(db, company_id="HQ01"):

        return db.query(Location).filter(
            Location.company_id == company_id,
            Location.use_yn == "Y"
        ).first()


    @staticmethod
    def check_in(db, user_id, req):

        device = db.query(Device).filter(
            Device.device_id == req.device_id,
            Device.user_id == user_id,
            Device.status == "APPROVED"
        ).first()

        print(req.device_id)

        if not device:
            return {"result": "FAIL", "msg": "장치 미등록"}
        elif device.status != "APPROVED":
            return {"result": "FAIL", "msg": "장치 미승인"}
            
        emp_id = device.emp_id

        company = db.query(Location).filter(
            Location.use_yn == "Y"
        ).first()

        if not company:
            return {"result": "FAIL", "msg": "회사 위치 없음"}

        today = datetime.now().date()

        dist = self._distance_m(company.lat, company.lng, req.lat, req.lng)

        if dist > company.accuracy:
            error_msg = f"출근 가능 지역 아님 ({int(dist)}m / 허용 {company.accuracy}m)"
            db.commit()
            
            return {"result": "FAIL", "msg": error_msg}

        exists = db.query(Attendance).filter(
            Attendance.emp_id == emp_id,
            Attendance.user_id == user_id,
            Attendance.work_date == today
        ).first()

        #if exists is None:
        if not exists:
            att = Attendance(
                emp_id=emp_id,
                user_id=user_id,
                work_date=today,
                in_time=datetime.now(),
                in_lat=req.lat,
                in_lng=req.lng,
                status="IN"
            )

            db.add(att)
            db.commit()

            return {
                "result":"OK",
                "msg":"자동 출근 완료"
            }

        return {
            "result":"OK",
            "msg":"이미 출근했습니다."
        }


    @staticmethod
    def _distance_m(lat1, lng1, lat2, lng2):
        from math import radians, sin, cos, sqrt, atan2

        radius = 6371000
        lat1_r = radians(lat1)
        lon1_r = radians(lng1)
        lat2_r = radians(lat2)
        lon2_r = radians(lng2)

        dlat = lat2_r - lat1_r
        dlon = lon2_r - lon1_r
        a = sin(dlat / 2) ** 2 + cos(lat1_r) * cos(lat2_r) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return radius * c

    @staticmethod
    def check_out(db, user_id, req):

        device = db.query(Device).filter(
            Device.device_id == req.device_id,
            Device.user_id == user_id,
            Device.status == "APPROVED"
        ).first()

        emp_id = device.emp_id

        if not device:
            return {
                "result":"FAIL",
                "msg":"등록되지 않은 장치"
            }

        today = datetime.now().date()

        att = db.query(Attendance).filter(
            Attendance.emp_id == emp_id,
            Attendance.user_id == user_id,
            Attendance.work_date == today
        ).first()

        if not att:
            return {
                "result":"FAIL",
                "msg":"출근 기록 없음"
            }

        if att.out_time:
            return {
                "result":"FAIL",
                "msg":"이미 퇴근 처리됨"
            }

        att.out_time = datetime.now()
        att.out_lat = req.lat
        att.out_lng = req.lng
        att.status = "OUT"

        db.commit()

        return {
            "result":"OK",
            "msg":"퇴근 완료"
        }