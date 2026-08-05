from sqlalchemy.orm import Session

from app.models.device import Device
from app.models.employee import Employee
from app.repository.device_repository import DeviceRepository


class DeviceService:

    ############################################################
    # 디바이스목록
    ############################################################
    @staticmethod
    def list(db: Session,
            device_name="",
            login_id="",
            status=""):
        
        rows = DeviceRepository.list(
            db,
            device_name,
            login_id,
            status
        )

        result = []

        for row in rows:
            login_id_value = getattr(row, "user_id", None)
            if login_id_value is None:
                login_id_value = getattr(row, "login_id", "")

            result.append({
                "device_id": row.device_id,
                "emp_id": row.emp_id,
                "login_id": login_id_value,
                "device_name": row.device_name,
                "device_type": row.device_type,
                "phone_hash": row.phone_hash,
                "status": row.status,
                "reg_date": row.reg_date,
                "approved_date": row.approved_date
            })

        return result
    
    ############################################################
    # 디바이스 등록 요청
    ############################################################
    @staticmethod
    def create(
        db,
        login_id,
        device_id,
        device_name
    ):

        device = db.query(Device).filter(
            Device.device_id == device_id
        ).first()

        if device:
            return {
                "result":"FAIL",
                "msg":"이미 등록된 장치"
            }
        
        employee = db.query(Employee).filter(
            Employee.login_id == login_id
        ).first()

        emp_id = ""
        if not employee:
            return {
                "result":"FAIL",
                "msg":"미 등록 아이디"
            }
        elif employee.use_yn == "N":
            return {
                "result":"FAIL",
                "msg":"사용불가 아이디"
            }
        else:
            emp_id = employee.emp_id

        if emp_id == "":
            return {
                "result":"FAIL",
                "msg":"미 확인 아이디"
            }

        new_device = Device(
            device_id=device_id,
            emp_id=employee.emp_id,
            user_id=employee.login_id,
            device_name=device_name,
            status="PENDING"
        )

        db.add(new_device)
        db.commit()

        return {
            "result":"OK",
            "msg":"승인 대기중"
        }

    ############################################################
    # 디바이스 승인
    ############################################################
    def approve(db, device_id):

        device = db.query(Device).filter(
            Device.device_id == device_id
        ).first()

        if not device:
            return {"result": "FAIL", "msg": "없음"}

        device.status = "APPROVED"
        db.commit()

        return {"result": "OK", "msg": "승인 완료"}
    
    ############################################################
    # 디바이스 거부
    ############################################################
    def reject(db, device_id):

        device = db.query(Device).filter(
            Device.device_id == device_id
        ).first()

        if not device:
            return {"result": "FAIL", "msg": "없음"}

        device.status = "REJECTED"
        db.commit()

        return {"result": "OK", "msg": "승인거부 완료"}
