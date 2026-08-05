async function login(){
    const id =
    document.getElementById("id").value;

    const pwd =
    document.getElementById("pwd").value;

    if(!id || !pwd){
        alert("아이디와 비밀번호를 입력하세요.");
        return;
    }

    const res = await fetch(
        "/login?user_id="
        + id +
        "&password=" +
        pwd,
        {
            method:"POST"
        }
    );

    const result = await res.json();
    const message = result && typeof result.msg === "string" && result.msg.trim()
        ? result.msg
        : (result && result.result === "OK" ? "로그인에 성공했습니다." : "로그인에 실패했습니다.");

    alert(message);

    if(result.result=="OK"){
        
        const empName = (result && (result.emp_name || result.name)) || id.toUpperCase();

        localStorage.setItem(
            "token",
            result.token
        );
        localStorage.setItem(
            "login_id",
            id.toUpperCase()
        );
        localStorage.setItem(
            "emp_name",
            empName
        );
        localStorage.setItem(
            "company_id",
            companyId
        );
        localStorage.setItem(
            "loc_code",
            locCode
        );

        location.href=
        "/web/dashboard/index.html";
    }
}