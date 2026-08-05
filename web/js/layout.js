async function initializeLayout() {
    await loadLayout();
    initUser();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeLayout);
} else {
    initializeLayout();
}

async function loadLayout() {

    document.getElementById("header").innerHTML =
        await (await fetch("/web/include/header.html")).text();

    document.getElementById("menu").innerHTML =
        await (await fetch("/web/include/menu.html")).text();

    document.getElementById("footer").innerHTML =
        await (await fetch("/web/include/footer.html")).text();
}

function renderUserName() {
    const loginUserEl = document.getElementById("loginUser");
    const authActionsEl = document.getElementById("authActions");

    if (!loginUserEl || !authActionsEl) {
        return false;
    }

    const token = localStorage.getItem("token");
    if (!token) {
        window.location.href = "/web/login/login.html";
        return false;
    }
    else {
        const empName = localStorage.getItem("emp_name") || localStorage.getItem("login_id") || "사용자";
        loginUserEl.textContent = `${empName}(${localStorage.getItem("login_id")})님 반갑습니다.`;
        authActionsEl.innerHTML = '<img src="/web/img/logout_bk_24.png" width="30" alt="로그아웃" onclick="logout()" style="cursor:pointer; margin-left:8px;">';
    }
    return true;

}

function logout() {
    localStorage.removeItem("token");
    localStorage.removeItem("login_id");
    localStorage.removeItem("emp_name");
    localStorage.removeItem("user_name");
    localStorage.removeItem("role");
    localStorage.removeItem("device_id");
    location.href = "/web/login/login.html";
}

function initUser() {

    if (!renderUserName()) {
        setTimeout(renderUserName, 50);
    }

    const token = localStorage.getItem("token");
    if (!token) {
        return;
    }

    const role = localStorage.getItem("role");

    if(role!="ADMIN"){

        /*
        document.getElementById("adminMenu").style.display="none";
        */

        const admin = document.getElementById("adminMenu");

        if(admin){
            admin.style.display = "none";
        }

    }

}