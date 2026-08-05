/**************************************************************************
 * employee.js
 * 직원관리
 **************************************************************************/

let employeeList = [];

/********************************************************
 * 최초 조회
 ********************************************************/
async function loadEmployee() {

    const emp_no = document.getElementById("emp_no").value.trim();
    const emp_name = document.getElementById("emp_name").value.trim();
    const dept_cd = document.getElementById("dept_cd").value;
    const status = document.getElementById("status").value;

    const url =
        "/employee/list"
        + "?emp_no=" + encodeURIComponent(emp_no)
        + "&emp_name=" + encodeURIComponent(emp_name)
        + "&dept_cd=" + encodeURIComponent(dept_cd)
        + "&status=" + encodeURIComponent(status);

    try{
        const response = await fetch(url);

        if(!response.ok){
            alert("직원조회 실패");
            return;
        }

        employeeList = await response.json();
        drawEmployee(employeeList);
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }

}

/********************************************************
 * Grid 출력
 ********************************************************/
function drawEmployee(data){

    const tbody =document.querySelector("#tblData tbody");

    tbody.innerHTML = "";

    if(data.length==0){

        tbody.innerHTML =
        `<tr>
            <td colspan="9">
                조회된 데이터가 없습니다.
            </td>
        </tr>`;

        return;
    }

    data.forEach(emp=>{

        let badge="";

        switch(emp.status){
            case "ACTIVE":
                badge="<span class='badge badge-green'>재직</span>";
                break;

            case "LEAVE":
                badge="<span class='badge badge-yellow'>휴직</span>";
                break;

            case "RETIRE":
                badge="<span class='badge badge-gray'>퇴사</span>";
                break;

            default:
                badge=emp.status;
        }

        tbody.innerHTML+=`
        <tr>
            <td>
                <input type="checkbox" class="chkEmp" value="${emp.emp_id}">
            </td>
            <td>${emp.emp_no}</td>
            <td>${emp.emp_name}</td>
            <td>${emp.dept_name ?? ""}</td>
            <td>${emp.position_name ?? ""}</td>
            <td>${emp.phone ?? ""}</td>
            <td>${emp.join_date ?? ""}</td>
            <td>${badge}</td>
            <td>
                <button class="btn-edit" onclick="employeeEdit(${emp.emp_id})">수정</button>
                <button class="btn-del" onclick="employeeDelete(${emp.emp_id})">삭제</button>
            </td>
        </tr>
        `;
    });

}

/********************************************************
 * 조회조건 초기화
 ********************************************************/
function searchReset(){
    document.getElementById("emp_no").value="";
    document.getElementById("emp_name").value="";
    document.getElementById("dept_cd").value="";
    document.getElementById("status").value="";

    loadEmployee();
}

/********************************************************
 * 신규등록
 ********************************************************/
function employeeAdd(){
    location.href="/web/employee/empadd.html";
}

/********************************************************
 * 수정
 ********************************************************/
function employeeEdit(emp_id){
    location.href=
        "/web/employee/empedit.html?emp_id="+emp_id;
}

/********************************************************
 * 삭제
 ********************************************************/
async function employeeDelete(emp_id){

    if(!confirm("삭제하시겠습니까?")){
        return;
    }

    const response =
        await fetch(
            "/employee/"+emp_id,
            {
                method:"DELETE"
            }
        );

    if(response.ok){
        alert("삭제되었습니다.");
        loadEmployee();
    }
    else{
        alert("삭제 실패");
    }
}

/********************************************************
 * 전체선택
 ********************************************************/
function checkAll(obj){

    const chk=
        document.querySelectorAll(".chkEmp");

    chk.forEach(c=>{
        c.checked=obj.checked;
    });

}

/********************************************************
 * 선택삭제
 ********************************************************/
async function deleteChecked(){

    const chk=
        document.querySelectorAll(".chkEmp:checked");

    if(chk.length==0){
        alert("선택된 직원이 없습니다.");
        return;
    }

    if(!confirm("선택 삭제하시겠습니까?")){
        return;
    }

    for(let c of chk){

        await fetch(
            "/employee/"+c.value,
            {
                method:"DELETE"
            }
        );
    }

    loadEmployee();
}



/********************************************************
 * 신규저장
 ********************************************************/
async function saveAddEmployee() {

    const emp_no = document.getElementById("emp_no").value.trim();
    const emp_name = document.getElementById("emp_name").value.trim();
    const login_id = document.getElementById("login_id").value.trim();
    const pwd = document.getElementById("pwd").value.trim();
    const pwd_chk = document.getElementById("pwd_chk").value.trim();
    const dept_cd = document.getElementById("dept_cd").value.trim();
    const position_cd = document.getElementById("position_cd").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const join_date = document.getElementById("join_date").value;
    const status = document.getElementById("status").value;
    const use_yn = document.getElementById("use_yn").value;
    const gps_id = document.getElementById("gps_id").value.trim(); //GPS회사코드
    const gps_code = document.getElementById("gps_code").value.trim(); //GPS코드

    /* Validation */
    if(emp_no==""){
        alert("사원번호를 입력하세요.");
        document.getElementById("emp_no").focus();
        return;
    }

    if(emp_name==""){
        alert("사원명을 입력하세요.");
        document.getElementById("emp_name").focus();
        return;
    }

    if(login_id==""){
        alert("로그인 아이디를 입력하세요.");
        document.getElementById("login_id").focus();
        return;
    }

    if(pwd!=pwd_chk){
        alert("비밀번호와 비밀번호 확인 항목 입력 내용이 다릅니다..");
        document.getElementById("pwd_chk").focus();
        return;
    }

    /*
    if(!idChecked){

        alert("아이디 중복확인을 해주세요.");

        return;
    }
    */

    document.getElementById("login_id").addEventListener("input",function(){

    idChecked=false;

    document.getElementById("idMsg").innerHTML="";



    const regex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=]).{8,20}$/;

        if(!regex.test(pwd)){

            alert(
                "비밀번호는 8~20자이며 영문 대/소문자, 숫자, 특수문자를 모두 포함해야 합니다."
            );

            return;
        }

    });

    const body={
        emp_no:emp_no,
        login_id:login_id,
        password:pwd,
        emp_name:emp_name,
        dept_cd:dept_cd,
        position_cd:position_cd,
        duty_cd:null,
        phone: phone || "",
        email:null,
        join_date:join_date,
        company_id:gps_id || "",
        loc_code:gps_code || "",
        status:status,
        use_yn:use_yn
    };

    try{
        const response =
            await fetch(
                "/employee",
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
            location.href="/web/employee/empList.html";
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


/********************************************************
 * 아이디중복검사
 ********************************************************/
async function checkUserId(){

    const login_id =
        document.getElementById("login_id").value.trim();

    if(login_id==""){

        alert("로그인 아이디를 입력하세요.");

        return;
    }

    const res = await fetch(

        "/employee/check?login_id="+encodeURIComponent(login_id)

    );

    const result = await res.json();

    const msg=document.getElementById("idMsg");

    alert(result.msg);

    if(result.result=="OK"){

        msg.style.color="blue";
        msg.innerHTML="사용 가능한 아이디입니다.";

        idChecked=true;

    }
    else{

        msg.style.color="red";
        msg.innerHTML="이미 사용중인 아이디입니다.";

        idChecked=false;

    }

}

/********************************************************
 * 비밀번호 일치 검증
 ********************************************************/
function checkPassword(){

    const pwd =
        document.getElementById("pwd").value;

    let score=0;

    if(pwd.length>=8)
        score++;

    if(/[A-Z]/.test(pwd))
        score++;

    if(/[a-z]/.test(pwd))
        score++;

    if(/[0-9]/.test(pwd))
        score++;

    if(/[!@#$%^&*()_+\-=]/.test(pwd))
        score++;

    const div =
        document.getElementById("pwdStrength");

    switch(score){

        case 0:
        case 1:

            div.innerHTML="🔴 매우 약함";
            div.style.color="red";

            break;

        case 2:

            div.innerHTML="🟠 약함";
            div.style.color="orange";

            break;

        case 3:

            div.innerHTML="🟡 보통";
            div.style.color="#d6a300";

            break;

        case 4:

            div.innerHTML="🟢 강함";
            div.style.color="green";

            break;

        case 5:

            div.innerHTML="🟢 매우 강함";
            div.style.color="darkgreen";

            break;

    }

}

/*************************************************
 * 부서 찾기
 *************************************************/
function popupDepartment(){
    window.open(
        "/web/employee/deptpopup.html",
        "dept",
        "width=650,height=420"
    );
}


/*************************************************
 * 부서 선택
 *************************************************/
function setParentDept(cd,name){
    document.getElementById("dept_cd").value=cd;
}

/*************************************************
 * 출퇴근 회사 GPS 찾기
 *************************************************/
function popupLocation(){
    window.open(
        "/web/location/locpopup.html",
        "location",
        "width=650,height=420"
    );
}


/*************************************************
 * 출퇴근 회사 GPS 선택
 *************************************************/
function setParentLocation(id,cd,name){
    document.getElementById("gps_id").value=id;
    document.getElementById("gps_code").value=cd;
    document.getElementById("gps_name").value=name;
}

/********************************************************
 * 수정조회
 ********************************************************/
async function loadEditEmployee(){

    const res = await fetch("/employee/" + encodeURIComponent(emp_id));

    if(!res.ok){
        alert("직원 상세를 찾을 수 없습니다.");
        return;
    }

    const data = await res.json();

    document.getElementById("emp_id").value = data.emp_id;
    document.getElementById("emp_no").value = data.emp_no;
    document.getElementById("login_id").value = data.login_id;
    document.getElementById("emp_name").value = data.emp_name;
    document.getElementById("pwd").value = data.pwd;
    document.getElementById("pwd_chk").value = data.pwd;

    document.getElementById("dept_cd").value = data.dept_cd ?? "";
    document.getElementById("position_cd").value = data.position_cd ?? "";
    //document.getElementById("phone").value = data.phone;
    document.getElementById("join_date").value = data.join_date ?? "";
    document.getElementById("status").value = data.status;
    document.getElementById("use_yn").value = data.use_yn;

}
/********************************************************
 * 수정저장
 ********************************************************/
async function saveEditEmployee(){

    const emp_id = document.getElementById("emp_id").value;

    if (!emp_id) {
        alert("직원 ID가 존재하지 않습니다.");
        return;
    }

    const pwdValue = document.getElementById("pwd").value;
    const password = pwdValue.trim() !== "" ? pwdValue : null;

    const body={
        login_id: document.getElementById("login_id").value,
        password: password,
        emp_name: document.getElementById("emp_name").value,
        dept_cd: document.getElementById("dept_cd").value,
        position_cd: document.getElementById("position_cd").value,
        duty_cd:null,
        phone: document.getElementById("phone").value,
        email:null,
        join_date: document.getElementById("join_date").value,
        status: document.getElementById("status").value,
        use_yn: document.getElementById("use_yn").value,
        company_id: document.getElementById("gps_id").value.trim(), //GPS회사코드
        loc_code: document.getElementById("gps_code").value.trim() //GPS코드
    };

    try {
        const response =
            await fetch(
                "/employee/" + encodeURIComponent(emp_id),
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

            location.href="/web/employee/empList.html";

        }else{

            const err=await response.json();

            alert(err.detail);

        }
    } catch (e) {
        console.error(e);
        alert("서버 연결 실패");
    }
}