from sqlalchemy.orm import Session

from app.models.department import Department
from app.repository.department_repository_tree import DepartmentTreeRepository


class DepartmentTreeService:

    ############################################################
    # 부서목록
    ############################################################
    @staticmethod
    def list(
            db: Session,
            dept_name: str = "",
            sort_no=None,
            use_yn: str = "",
            dept_cd: str = ""
    ):

        rows = DepartmentTreeRepository.list(
            db=db,
            dept_name=dept_name,
            sort_no=sort_no,
            use_yn=use_yn,
            dept_cd=dept_cd
        )

        result = []

        for dept, emp_count in rows:

            result.append({

                "dept_cd": dept.dept_cd,
                "dept_name": dept.dept_name,
                "parent_cd": dept.parent_cd,
                "sort_no": dept.sort_no,
                "use_yn": dept.use_yn,
                "remark": dept.remark,
                "emp_count": emp_count

            })

        return result

    ############################################################
    # Tree
    ############################################################
    @staticmethod
    def tree(db: Session):

        rows = DepartmentTreeRepository.tree(db)

        nodes = {}

        for row in rows:

            nodes[row.dept_cd] = {

                "dept_cd": row.dept_cd,
                "dept_name": row.dept_name,
                "parent_cd": row.parent_cd,
                "sort_no": row.sort_no,
                "use_yn": row.use_yn,
                "children": []

            }

        root = []

        for node in nodes.values():

            parent = node["parent_cd"]

            if parent and parent in nodes:

                nodes[parent]["children"].append(node)

            else:

                root.append(node)

        return root

    ############################################################
    # 부서조회
    ############################################################
    @staticmethod
    def get(
            db: Session,
            dept_cd: str
    ):

        row = DepartmentTreeRepository.get(
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
            "use_yn": row.use_yn,
            "remark": row.remark

        }

    ############################################################
    # 등록
    ############################################################
    @staticmethod
    def create(
            db: Session,
            dto
    ):

        exists = DepartmentTreeRepository.get(
            db,
            dto.dept_cd
        )

        if exists:

            raise Exception("이미 존재하는 부서코드입니다.")

        if dto.parent_cd:

            parent = DepartmentTreeRepository.get(
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
        department.remark = dto.remark

        DepartmentTreeRepository.insert(
            db,
            department
        )

        return department

    ############################################################
    # 수정
    ############################################################
    @staticmethod
    def update(
            db: Session,
            dept_cd: str,
            dto
    ):

        department = DepartmentTreeRepository.get(
            db,
            dept_cd
        )

        if department is None:

            raise Exception("부서를 찾을 수 없습니다.")

        if dto.parent_cd == dept_cd:

            raise Exception("자기 자신을 부모부서로 지정할 수 없습니다.")

        if dto.parent_cd:

            parent = DepartmentTreeRepository.get(
                db,
                dto.parent_cd
            )

            if parent is None:

                raise Exception("부모부서가 존재하지 않습니다.")

        department.dept_name = dto.dept_name
        department.parent_cd = dto.parent_cd
        department.sort_no = dto.sort_no
        department.use_yn = dto.use_yn
        department.remark = dto.remark

        DepartmentTreeRepository.update(db)

        return department

    ############################################################
    # 삭제
    ############################################################
    @staticmethod
    def delete(
            db: Session,
            dept_cd: str
    ):

        rows = DepartmentTreeRepository.tree(db)

        for row in rows:

            if row.parent_cd == dept_cd:

                raise Exception(
                    "하위부서가 존재하여 삭제할 수 없습니다."
                )

        result = DepartmentTreeRepository.delete(
            db,
            dept_cd
        )

        if result is False:

            raise Exception(
                "삭제할 부서가 존재하지 않습니다."
            )

        return True

    ############################################################
    # 사용여부 변경
    ############################################################
    @staticmethod
    def change_use_yn(
            db: Session,
            dept_cd: str,
            use_yn: str
    ):

        result = DepartmentTreeRepository.update_use_yn(
            db,
            dept_cd,
            use_yn
        )

        if result is False:

            raise Exception("부서를 찾을 수 없습니다.")

        return True