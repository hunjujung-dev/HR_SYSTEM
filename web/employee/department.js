/**************************************************************************
 * department.js
 * 부서관리
 **************************************************************************/

let departmentList = [];

/********************************************************
 * 최초 조회
 ********************************************************/
async function loadDepartment() {

    const dept_name = document.getElementById("dept_name").value.trim();
    const sort_no = document.getElementById("sort_no").value;
    const use_yn = document.getElementById("use_yn").value;

    const url =
        "/department/list"
        + "?dept_name=" + encodeURIComponent(dept_name)
        + "&sort_no=" + sort_no
        + "&use_yn=" + encodeURIComponent(use_yn);

    try{
        const response = await fetch(url);
        if(!response.ok){
            alert("부서조회 실패");
            return;
        }

        departmentList = await response.json();

        drawDepartment(departmentList);
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }
}

/********************************************************
 * Grid 출력
 ********************************************************/
function drawDepartment(data){

    const tbody =
        document.querySelector("#tblData tbody");

    tbody.innerHTML = "";

    if(data.length==0){
        tbody.innerHTML =
        `<tr>
            <td colspan="7">
                조회된 데이터가 없습니다.
            </td>
        </tr>`;

        return;

    }

    data.forEach(dept=>{

        let badge="";

        switch(dept.use_yn){
            case "Y":
                badge="<span class='badge badge-green'>예</span>";
                break;
            case "N":
                badge="<span class='badge badge-gray'>아니오</span>";
                break;
            default:
                badge=dept.use_yn;
        }

        tbody.innerHTML+=`
        <tr>
            <td>
                <input type="checkbox" class="chkDept" value="${dept.dept_cd}">
            </td>
            <td>${dept.dept_cd}</td>
            <td>${dept.dept_name}</td>
            <td>${dept.parent_cd ?? ""}</td>
            <td>${dept.sort_no ?? 1}</td>
            <td>${badge}</td>
            <td>
                <button class="btn-edit" onclick="departmentEdit('${dept.dept_cd}')">수정</button>
                <button class="btn-del" onclick="departmentDelete(${dept.dept_cd})">삭제</button>
            </td>
        </tr>
        `;
    });
}

/********************************************************
 * 조회조건 초기화
 ********************************************************/
function searchReset(){
    document.getElementById("dept_name").value="";
    document.getElementById("sort_no").value="";
    document.getElementById("use_yn").value="";
    loadDepartment();
}

/********************************************************
 * 신규등록
 ********************************************************/
function departmentAdd(){
    location.href="/web/employee/deptadd.html";
}

/*************************************************
 * 신규저장
 *************************************************/
async function saveAddDepartment(){
    const dept_cd = document.getElementById("dept_cd").value.trim();
    const dept_name = document.getElementById("dept_name").value.trim();
    const parent_cd = document.getElementById("parent_cd").value.trim();
    const sort_no = document.getElementById("sort_no").value;
    const use_yn = document.getElementById("use_yn").value;

    /* Validation */
    if(dept_cd==""){
        alert("부서코드를 입력하세요.");
        document.getElementById("dept_cd").focus();
        return;
    }

    if(dept_name==""){
        alert("부서명을 입력하세요.");
        document.getElementById("dept_name").focus();
        return;
    }

    const body={
        dept_cd:dept_cd,
        dept_name:dept_name,
        parent_cd:parent_cd,
        sort_no:Number(sort_no),
        use_yn:use_yn
    };

    try{
        const response =
            await fetch(
                "/department",
                {
                    method:"POST",
                    headers:{
                        "Content-Type":"application/json"
                    },
                    body:JSON.stringify(body)
                }
            );
        if(response.ok){
            alert("등록되었습니다.");
            location.href="/web/employee/deptList.html";
        }
        else{
            const err = await response.json();
            alert(err.detail);
        }
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }
}

/*************************************************
 * 부모부서 찾기
 *************************************************/
function popupDepartment(){
    window.open(
        "/web/employee/deptpopup.html",
        "dept",
        "width=650,height=420"
    );
}


/*************************************************
 * 부모부서 선택
 *************************************************/
function setParentDept(cd,name){
    document.getElementById("parent_cd").value=cd;
}

/********************************************************
 * 수정
 ********************************************************/
function departmentEdit(dept_cd){
    location.href="/web/employee/deptedit.html?dept_cd="+encodeURIComponent(dept_cd);
}

/********************************************************
 * 수정조회
 ********************************************************/
async function loadEditDepartment(){

    const res = await fetch("/department/" + encodeURIComponent(dept_cd));

    if(!res.ok){
        alert("부서를 찾을 수 없습니다.");
        return;
    }

    const data = await res.json();

    document.getElementById("dept_cd").value = data.dept_cd;
    document.getElementById("dept_name").value = data.dept_name;
    document.getElementById("parent_cd").value = data.parent_cd ?? "";
    document.getElementById("sort_no").value = data.sort_no ?? 0;
    document.getElementById("use_yn").value = data.use_yn;

}/********************************************************
 * 수정저장
 ********************************************************/
async function saveEditDepartment(){

    const dept_cd =
        document.getElementById("dept_cd").value;

    const body={
        dept_name: document.getElementById("dept_name").value,
        parent_cd: document.getElementById("parent_cd").value,
        sort_no: Number(document.getElementById("sort_no").value),
        use_yn: document.getElementById("use_yn").value
    };

    const response =
        await fetch(
            "/department/" + encodeURIComponent(dept_cd),
            {
                method:"PUT",
                headers:{
                    "Content-Type":"application/json"
                },
                body:JSON.stringify(body)
            }
        );

    if(response.ok){

        alert("수정되었습니다.");

        location.href="/web/employee/deptlist.html";

    }else{

        const err=await response.json();

        alert(err.detail);

    }

}


/********************************************************
 * 삭제
 ********************************************************/
async function departmentDelete(dept_cd){
    if(!confirm("삭제하시겠습니까?")){
        return;
    }

    const response =
        await fetch(
            "/department/"+dept_cd,
            {
                method:"DELETE"
            }
        );

    if(response.ok){
        alert("삭제되었습니다.");
        loadDepartment();
    }
    else{
        alert("삭제 실패");
    }

}

/********************************************************
 * 전체선택
 ********************************************************/
function checkAll(obj){

    const chk=document.querySelectorAll(".chkDept");

    chk.forEach(c=>{
        c.checked=obj.checked;
    });
}

/********************************************************
 * 선택삭제
 ********************************************************/
async function deleteChecked(){

    const chk=document.querySelectorAll(".chkDept:checked");

    if(chk.length==0){
        alert("선택된 부서가 없습니다.");
        return;
    }

    if(!confirm("선택 삭제하시겠습니까?")){
        return;
    }

    for(let c of chk){
        await fetch(
            "/department/"+c.value,
            {
                method:"DELETE"
            }
        );
    }
    loadDepartment();
}

/**************************************************************************
 * PopUp(department_popup.js)
 **************************************************************************/

async function loadDepartmentPopup(){
    const dept_name = document.getElementById("search_name").value;
    const response =
        await fetch(
            "/department/list?dept_name="
            + encodeURIComponent(dept_name)
        );
    const data = await response.json();
    drawPopup(data);
}

function drawPopup(data){
    const tbody = document.querySelector("#tblPopup tbody");

    let html="";

    data.forEach(d=>{
        html += `
        <tr>
            <td>${d.dept_cd}</td>
            <td>${d.dept_name}</td>
            <td align='center'>
                <button onclick="selectDepartment('${d.dept_cd}','${d.dept_name}')">선택</button>
            </td>
        </tr>
        `;
    });

    tbody.innerHTML = html;
}

function selectDepartment(cd,name){
    window.opener.setParentDept(cd,name);
    window.close();
}

