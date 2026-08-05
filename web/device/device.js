/**************************************************************************
 * device.js
 * 장치관리
 **************************************************************************/

let deviceList = [];

/********************************************************
 * 최초 목록 조회
 ********************************************************/
async function loadDeviceList() {

    const device_name = document.getElementById("device_name").value.trim();
    const login_id = document.getElementById("login_id").value.trim();
    const status = document.getElementById("status").value;

    const url =
        "/device/list"
        + "?device_name=" + encodeURIComponent(device_name)
        + "&login_id=" + encodeURIComponent(login_id)
        + "&status=" + encodeURIComponent(status);

    try{
        const response = await fetch(url);
        if(!response.ok){
            alert("장치조회 실패");
            return;
        }

        deviceList = await response.json();

        drawDevice(deviceList);
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }
}

/********************************************************
 * Grid 출력
 ********************************************************/
function drawDevice(data){

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

    data.forEach(device=>{

        let statusText = "";
        let action = "";

        switch(device.status){
            case "APPROVED":
                statusText = `
                    <span class="status-approved">
                        승인
                    </span>`;
                action = "";
                break;
                
            case "REJECTED":
                statusText = `
                    <span class="status-rejected">
                        거부
                    </span>`;
                action = "";
                break;

            case "PENDING":
                statusText = `
                    <span class="status-pending">
                        대기
                    </span>`;
                action = `
                    <button class="btn-edit"
                        onclick="approve('${device.device_id}')">
                        승인
                    </button>

                    <button class="btn-del"
                            onclick="reject('${device.device_id}')">
                        거부
                    </button>`;
                break;

            default:
                statusText = device.status;
                action = "";
        }

        tbody.innerHTML+=`
        <tr>
            <td>
                <input type="checkbox" class="chkDevice" value="${device.device_id}">
            </td>
            <td>${device.device_id}</td>
            <td>${device.device_name}</td>
            <td>${device.device_type}</td>
            <td>${device.login_id}</td>
            <td>${device.login_id}</td>
            <td>${device.phone_hash}</td>
            <td>${statusText}</td>
            <td>${device.reg_date ?? ""}</td>
            <td>${device.approved_date ?? ""}</td>
            <td>${action}</td>
        </tr>
        `;
    });
}


/********************************************************
 * 조회조건 초기화
 ********************************************************/
function searchReset(){
    document.getElementById("device_name").value="";
    document.getElementById("login_id").value="";
    document.getElementById("status").value="";
    loadDeviceList();
}

/********************************************************
 * 장치 등록 요청
 ********************************************************/
async function saveAddDevice() {

    let deviceId = localStorage.getItem("device_id");

    if (!deviceId) {
        deviceId = crypto.randomUUID();
        localStorage.setItem("device_id", deviceId);
    }

    const login_id =
        document.getElementById("login_id").value;

    const device_name = navigator.userAgent;

    const data = {
        login_id: login_id,
        device_id: deviceId,
        device_name: device_name
    };
    const res = await fetch("/device", {
        method: "POST",
        headers: {
            "Content-Type":"application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();

    alert(result.msg);
}

/********************************************************
 * 장치 등록요청 승인
 ********************************************************/
async function approve(device_id) {

    if(!confirm("선택한 장치를 승인하시겠습니까?")){
        return;
    }

    const login_id = document.getElementById("login_id")?.value?.trim() ?? "";

    const res = await fetch("/device/approve", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({device_id, login_id})
    });

    const result = await res.json();

    alert(result.msg);

    loadDeviceList();
}

/********************************************************
 * 장치 등록요청 거부
 ********************************************************/
async function reject(device_id){

    if(!confirm("선택한 장치를 거부하시겠습니까?")){
        return;
    }

    const login_id = document.getElementById("login_id")?.value?.trim() ?? "";

    const res = await fetch("/device/reject",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({
            device_id:device_id,
            login_id:login_id
        })

    });

    const result = await res.json();

    alert(result.msg);

    loadDeviceList();

}