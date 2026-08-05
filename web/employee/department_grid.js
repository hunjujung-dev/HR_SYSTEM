/**************************************************************************
 * department_grid.js
 * Grid 전용
 **************************************************************************/

let departmentList = [];

/*******************************************************
 * Grid 조회
 *******************************************************/
async function loadDepartmentGrid(dept_cd = "") {
    let url = "/department/list";
    if (dept_cd !== "") {
        url += "?dept_cd=" + encodeURIComponent(dept_cd);
    }

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("조회 실패");
        }

        departmentList = await response.json();
        drawDepartment(departmentList);
    }
    catch (e) {
        console.error(e);
        alert("부서 조회 실패");
    }

}

/*******************************************************
 * Grid 출력
 *******************************************************/
function drawDepartment(data) {

    const tbody = document.querySelector("#tblData tbody");

    if (!tbody) return;
    tbody.innerHTML = "";
    if (data.length === 0) {
        tbody.innerHTML = `        <tr>
            <td colspan="8">조회된 데이터가 없습니다.</td>
        </tr>`;
        return;
    }

    data.forEach(dept => {

        tbody.innerHTML += `
        <tr>
            <td>${dept.dept_cd}</td>
            <td>${dept.dept_name}</td>
            <td>${dept.parent_name ?? ""}</td>
            <td>${dept.sort_no}</td>
            <td>${dept.use_yn}</td>
            <td>${dept.emp_count ?? 0}</td>
            <td>
                <button class="btn-sm btn-primary" onclick="departmentEdit('${dept.dept_cd}')">수정</button>
                <button class="btn-sm btn-danger" onclick="departmentDelete('${dept.dept_cd}')">삭제</button>
            </td>
        </tr>
        `;
    });
}