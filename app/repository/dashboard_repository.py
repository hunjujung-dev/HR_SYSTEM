from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


class DashboardRepository:

    @staticmethod
    def get_dashboard(db):

        result = {}

        def safe_count(query_text):
            try:
                return db.execute(text(query_text)).scalar() or 0
            except SQLAlchemyError:
                return 0

        def safe_rows(query_text):
            try:
                return db.execute(text(query_text)).fetchall()
            except SQLAlchemyError:
                return []

        result["employee_count"] = safe_count("SELECT COUNT(*) FROM TB_EMPLOYEE")
        result["checkin_count"] = safe_count("""
            SELECT COUNT(*)
            FROM TB_ATTENDANCE
            WHERE WORK_DATE = CONVERT(date,GETDATE())
              AND IN_TIME IS NOT NULL
        """)
        result["checkout_count"] = safe_count("""
            SELECT COUNT(*)
            FROM TB_ATTENDANCE
            WHERE WORK_DATE = CONVERT(date,GETDATE())
              AND OUT_TIME IS NOT NULL
        """)
        result["pending_device"] = safe_count("SELECT COUNT(*) FROM TB_DEVICE WHERE STATUS = 'PENDING'")
        result["gps_company"] = safe_count("SELECT COUNT(*) FROM TB_COMPANY_location")
        result["today_work"] = safe_count("""
            SELECT COUNT(*)
            FROM TB_ATTENDANCE
            WHERE WORK_DATE = CONVERT(date,GETDATE())
              AND IN_TIME IS NOT NULL
              AND OUT_TIME IS NULL
        """)

        rows = safe_rows("""
            SELECT TOP 5
                E.EMP_NAME,
                CONVERT(varchar(5),A.IN_TIME,108) AS IN_TIME
            FROM TB_ATTENDANCE A
            JOIN TB_EMPLOYEE E ON A.EMP_ID = E.EMP_ID
            WHERE A.WORK_DATE = CONVERT(date,GETDATE())
            ORDER BY A.IN_TIME DESC
        """)
        result["recent_checkin"] = [
            {"name": r[0], "time": r[1]}
            for r in rows
        ]

        rows = safe_rows("""
            SELECT TOP 5 TITLE
            FROM TB_NOTICE
            ORDER BY NOTICE_DATE DESC
        """)
        result["notice"] = [
            {"title": r[0]}
            for r in rows
        ]

        return result