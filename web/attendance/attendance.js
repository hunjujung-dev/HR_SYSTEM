/**************************************************************************
 * attendance.js
 * 근태관리
 **************************************************************************/

let attendanceList = [];

/********************************************************
 * 최초 목록 조회
 ********************************************************/
async function loadAttendanceList() {

    const loginIdEl = document.getElementById("login_id");
    const workDateEl = document.getElementById("work_date");
    const statusEl = document.getElementById("status");

    const login_id = loginIdEl ? loginIdEl.value.trim() : "";
    const work_date = workDateEl ? workDateEl.value.trim() : "";
    const status = statusEl ? statusEl.value : "";

    const url =
        "/attendance/list"
        + "?login_id=" + encodeURIComponent(login_id)
        + "&work_date=" + encodeURIComponent(work_date)
        + "&status=" + encodeURIComponent(status);

    try{
        const response = await fetch(url);
        if(!response.ok){
            alert("근태 조회 실패");
            return;
        }

        attendanceList = await response.json();

        drawAttendance(attendanceList);
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }
}

function formatTime(value) {
    if (!value) {
        return "";
    }

    if (typeof value === "string") {
        const trimmed = value.trim();
        /*
        if (/^\d{1,2}:\d{1,2}:\d{1,2}/.test(trimmed)) {
            return trimmed.slice(0, 8);
        }
        */
       
        // 1. 문자열로 Date 객체 생성 가능한지 확인
        const date = new Date(trimmed);

       // 2. 올바른 날짜 데이터인 경우에만 포맷 변경 실행
        if (!isNaN(date.getTime())) {
            const year = date.getFullYear();
            const month = String(date.getMonth() + 1).padStart(2, '0');
            const day = String(date.getDate()).padStart(2, '0');
            const hours = String(date.getHours()).padStart(2, '0');
            const minutes = String(date.getMinutes()).padStart(2, '0');
            const seconds = String(date.getSeconds()).padStart(2, '0');
            
            return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
        }

        return trimmed;
    }

    return value;
}

function formatCoordinate(value) {
    if (value === null || value === undefined || value === "") {
        return "";
    }

    const numeric = Number(value);
    return Number.isFinite(numeric) ? numeric.toFixed(3) : value;
}

function formatStatus(value) {
    if (!value) {
        return "";
    }

    if (value.toUpperCase() === "IN") {
        return "출근";
    }
    if (value.toUpperCase() === "OUT") {
        return "퇴근";
    }
    return value;
}

function drawAttendance(list) {
    const tbody = document.querySelector("#tblData tbody");

    if (!tbody) {
        return;
    }

    tbody.innerHTML = "";

    if (!Array.isArray(list) || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9">조회된 데이터가 없습니다.</td></tr>';
        return;
    }

    list.forEach(item => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.login_id || ""}</td>
            <td>${item.work_date || ""}</td>
            <td>${formatTime(item.in_time)}</td>
            <td>${formatTime(item.out_time)}</td>
            <td>${formatCoordinate(item.in_lat)}</td>
            <td>${formatCoordinate(item.in_lng)}</td>
            <td>${formatCoordinate(item.out_lat)}</td>
            <td>${formatCoordinate(item.out_lng)}</td>
            <td>${formatStatus(item.status)}</td>
        `;
        tbody.appendChild(row);
    });
}

async function saveCheckIn() {

    let deviceId = localStorage.getItem("device_id");

    if (!deviceId) {
        deviceId = crypto.randomUUID();
        localStorage.setItem("device_id", deviceId);
    }

    const token = localStorage.getItem("token");
    const loginId = localStorage.getItem("login_id");

    if (!token || !loginId) {
        alert("로그인이 필요합니다.");
        location.href = "/web/login/login.html";
        return;
    }

    console.log(localStorage.getItem("token"));
    
    navigator.geolocation.getCurrentPosition(async (pos) => {

        const data = {
            emp_id: 0,
            user_id: loginId,
            work_date: new Date().toISOString().slice(0, 10),
            in_time: new Date().toTimeString().slice(0, 8),
            in_lat: pos.coords.latitude,
            in_lng: pos.coords.longitude,
            status: "IN"
        };

        const res = await fetch("/attendance/checkin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            body: JSON.stringify(data)
        });

        const result = await res.json();
        alert(result.msg);

    });
}


async function savecheckOut() {

    let deviceId = localStorage.getItem("device_id");

    if (!deviceId) {
        alert("디바이스 정보 미 존재")
    }
    else {

        const token = localStorage.getItem("token");
        
        navigator.geolocation.getCurrentPosition(async (pos) => {

            const data = {
                user_id: localStorage.getItem("login_id") || "",
                device_id: deviceId,
                lat: pos.coords.latitude,
                lng: pos.coords.longitude,
                accuracy: pos.coords.accuracy
            };
            
            const res = await fetch("/attendance/checkout", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token
                },
                body: JSON.stringify(data)
            });
            
            const result = await res.json();
            alert(result.msg);

        });
    }
}