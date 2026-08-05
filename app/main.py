from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# 최초 실행 시 테이블 자동 생성
from app.database import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount(
    "/web",
    StaticFiles(directory=BASE_DIR / "web"),
    name="web"
)

# 대쉬보드
from app.api.dashboard import router as dashboard_router
app.include_router(dashboard_router)

# 직원관리
from app.api.employee import router as employee_router
app.include_router(employee_router)

# 부서관리
from app.api.department import router as department_router
app.include_router(department_router)


# 조직도
from app.api.departmenttree import router as depttree_router
app.include_router(depttree_router)

# 디바이스
from app.api.device import router as device_router
app.include_router(device_router)

# 위치관리
from app.api.location import router as location_router
app.include_router(location_router)

# 출퇴근
from app.api.attendance import router as attendance_router
app.include_router(attendance_router)

# 로그인
from app.service.login_service import router as login_router
app.include_router(login_router)