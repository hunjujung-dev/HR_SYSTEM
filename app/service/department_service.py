from sqlalchemy.orm import Session

from app.models.department import Department
from app.repository.department_repository import DepartmentRepository


class DepartmentService:

    ############################################################
    # 부서목록
    ############################################################
    @staticmethod

    def list(db: Session,
             dept_name="",
            sort_no="",
            use_yn=""):

        rows = DepartmentRepository.list(
            db,
            dept_name,
            sort_no,
            use_yn)

        result = []

        for row in rows:
            result.append({
                "dept_cd": row.dept_cd,
                "dept_name": row.dept_name,
                "parent_cd": row.parent_cd,
                "sort_no": row.sort_no,
                "use_yn": row.use_yn
            })

        return result

    ############################################################
    # 부서조회
    ############################################################
    @staticmethod
    def get(
        db: Session,
        dept_cd: str
    ):

        row = DepartmentRepository.get(
            db,
            dept_cd
        )

        if row is None:

            return None

        return {

            "dept_cd": row.dept_cd,

            "dept_name": row.dept_name,

            "parent_cd": row.parent_cd,

            "sort_no": row.sort_no,

            "use_yn": row.use_yn

        }

    ############################################################
    # 부서등록
    ############################################################
    @staticmethod
    def create(
        db: Session,
        dto
    ):

        # 부서코드 중복 검사
        exists = DepartmentRepository.get(
            db,
            dto.dept_cd
        )

        if exists:

            raise Exception("이미 존재하는 부서코드입니다.")

        # 부모부서 존재 여부
        if dto.parent_cd:

            parent = DepartmentRepository.get(
                db,
                dto.parent_cd
            )

            if parent is None:

                raise Exception("부모부서가 존재하지 않습니다.")

        department = Department()

        department.dept_cd = dto.dept_cd
        department.dept_name = dto.dept_name
        department.parent_cd = dto.parent_cd
        department.sort_no = dto.sort_no
        department.use_yn = dto.use_yn

        DepartmentRepository.insert(
            db,
            department
        )

        return department

    ############################################################
    # 부서수정
    ############################################################
    @staticmethod
    def update(
        db: Session,
        dept_cd: str,
        dto
    ):

        department = DepartmentRepository.get(
            db,
            dept_cd
        )

        if department is None:

            raise Exception("부서가 존재하지 않습니다.")

        # 자기 자신을 부모부서로 지정 금지
        if dto.parent_cd == dept_cd:

            raise Exception("자기 자신을 부모부서로 지정할 수 없습니다.")

        # 부모부서 존재 여부
        if dto.parent_cd:

            parent = DepartmentRepository.get(
                db,
                dto.parent_cd
            )

            if parent is None:

                raise Exception("부모부서가 존재하지 않습니다.")

        department.dept_name = dto.dept_name
        department.parent_cd = dto.parent_cd
        department.sort_no = dto.sort_no
        department.use_yn = dto.use_yn

        DepartmentRepository.update(db)

        return department

    ############################################################
    # 부서삭제
    ############################################################
    @staticmethod
    def delete(
        db: Session,
        dept_cd: str
    ):

        # 하위부서 존재 여부
        rows = DepartmentRepository.list(db)

        for row in rows:

            if row.parent_cd == dept_cd:

                raise Exception(
                    "하위부서가 존재하여 삭제할 수 없습니다."
                )

        result = DepartmentRepository.delete(
            db,
            dept_cd
        )

        if not result:

            raise Exception(
                "삭제할 부서가 없습니다."
            )

        return True
    
    ############################################################
    # Tree 조회
    ############################################################
    @staticmethod
    def tree(db: Session):
        rows = DepartmentRepository.tree(db)

        dic = {}

        for row in rows:
            dic[row.dept_cd] = {
                "dept_cd": row.dept_cd,
                "dept_name": row.dept_name,
                "parent_cd": row.parent_cd,
                "sort_no": row.sort_no,
                "use_yn": row.use_yn,
                "children": []
            }

        roots = []

        for node in dic.values():
            parent = node["parent_cd"]
            if parent and parent in dic:
                dic[parent]["children"].append(node)
            else:
                roots.append(node)
        return roots