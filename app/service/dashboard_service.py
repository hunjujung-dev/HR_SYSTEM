from app.repository.dashboard_repository import DashboardRepository

class DashboardService:

    @staticmethod
    def get_dashboard(db):

        data = DashboardRepository.get_dashboard(db)

        # Chart 데이터 추가
        data["attendance_chart"] = {
            "labels":["출근","퇴근","근무중","승인대기"],
            "values":[
                data["checkin_count"],
                data["checkout_count"],
                data["today_work"],
                data["pending_device"]
            ]
        }

        data["dept_chart"] = {
            "labels":["물류","개발","관리","영업"],
            "values":[35,28,20,15]
        }

        return data