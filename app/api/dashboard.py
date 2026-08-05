from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.service.dashboard_service import DashboardService

router = APIRouter()

@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):

    return DashboardService.get_dashboard(db)