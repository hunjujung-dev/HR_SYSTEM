/**************************************************************************
 * location.js
 * 위치관리
 **************************************************************************/

let locationList = [];

/********************************************************
 * 최초 목록 조회
 ********************************************************/
async function loadLocationList() {

    const company_name = document.getElementById("company_name").value.trim();
    const use_yn = document.getElementById("use_yn").value;

    const url =
        "/location/list"
        + "?company_name=" + encodeURIComponent(company_name)
        + "&use_yn=" + encodeURIComponent(use_yn);

    try{
        const response = await fetch(url);
        if(!response.ok){
            alert("회사 위치조회 실패");
            return;
        }

        locationList = await response.json();

        drawLocation(locationList);
    }
    catch(e){
        console.error(e);
        alert("서버 연결 실패");
    }
}

/********************************************************
 * 신규등록
 ********************************************************/
function locationAdd(){
    location.href="/web/location/locadd.html";
}

/********************************************************
 * 수정
 ********************************************************/
function locationEdit(company_id, loc_code){
    location.href=
        "/web/location/locedit.html?company_id="+company_id+"&loc_code="+loc_code;
}


/********************************************************
 * Grid 출력
 ********************************************************/
function drawLocation(data){

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

    data.forEach(location=>{

        switch(location.use_yn){
            case "Y":
                UseYNText = "사용";
                break;
            case "N":
                UseYNText = "미사용";
                break;
            default:
                UseYNText = location.use_yn;
        }

        tbody.innerHTML+=`
        <tr>
            <td>
                <input type="checkbox" class="chkDevice" value="${location.company_id}">
            </td>
            <td>${location.company_id}</td>
            <td>${location.loc_code}</td>
            <td>${location.company_name}</td>
            <td>${location.lat}</td>
            <td>${location.lng}</td>
            <td>${location.accuracy}</td>
            <td>${UseYNText}</td>
            <td>${location.reg_date ?? ""}</td>
            <td><button class="btn-edit" onclick="locationEdit('${location.company_id}', ${location.loc_code})">수정</button></td>
        </tr>
        `;
    });
}


/********************************************************
 * 조회조건 초기화
 ********************************************************/
function searchReset(){
    document.getElementById("company_name").value="";
    document.getElementById("use_yn").value="";
    loadLocationList();
}

/********************************************************
 * 신규 등록
 ********************************************************/
async function saveAddLocation() {

    const company_id = (document.getElementById("company_id").value || "").trim() || "LOC" + Date.now();
    const company_name = (document.getElementById("company_name").value || "").trim() || "신규 회사";
    const loc_code = (document.getElementById("loc_code").value || "").trim();
    const lat = parseFloat(document.getElementById("lat").value);
    const lng = parseFloat(document.getElementById("lng").value);
    const accuracy = parseFloat(document.getElementById("accuracy").value);
    const remark = document.getElementById("remark").value;
    const use_yn = "Y";

    if(!company_id || !company_name || !loc_code){
        alert("회사코드, GPS코드, 회사명은 필수 입력입니다.");
        return;
    }
    if(!company_id.match(/^[a-zA-Z0-9]+$/)){
        alert("회사코드는 영문 대문자 또는 숫자만 가능합니다.");
        document.getElementById("company_id").focus();
        return;
    }
    if(!loc_code.match(/^[a-zA-Z0-9]+$/)){
        alert("GPS코드는 영문 대문자 또는 숫자만 가능합니다.");
        document.getElementById("loc_code").focus();
        return;
    }

    if (!/^[0-9]+$/.test(accuracy)) {
        alert("정확도는 숫자만 가능합니다.");
        document.getElementById("accuracy").focus();
        return;
    }

    if (!/^-?\d+(\.\d+)?$/.test(lat)) {
        alert("위도는 정수, 소수점 포함 숫자만 가능합니다.");
        document.getElementById("lat").focus();
        return;
    }
    if (!/^-?\d+(\.\d+)?$/.test(lng)) {
        alert("경도는 정수, 소수점 포함 숫자만 가능합니다.");
        document.getElementById("lng").focus();
        return;
    }

    if(lat < -90 || lat > 90 || lng < -180 || lng > 180){
        alert("위도는 -90~90, 경도는 -180~180 범위여야 합니다.");
        return;
    }

    const data = {
        company_id: company_id,
        company_name: company_name,
        loc_code: loc_code,
        lat: Number.isNaN(lat) ? 0 : lat,
        lng: Number.isNaN(lng) ? 0 : lng,
        accuracy: Number.isNaN(accuracy) ? 0 : accuracy,
        remark: remark || "",
        use_yn: use_yn
    };

    try{
        const response = await fetch("/location", {
            method: "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        });
        if(response.ok){
            alert("등록되었습니다.");
            location.href="/web/location/locList.html";
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
 * 수정조회
 ********************************************************/
async function loadEditLocation(){
    const params = new URLSearchParams(window.location.search);
    const company_id = params.get("company_id");
    const loc_code = params.get("loc_code");

    if (!company_id) {
        alert("회사 위치를 찾을 수 없습니다.1");
        return;
    }

    const res = await fetch(`/location/${encodeURIComponent(company_id)}/${encodeURIComponent(loc_code)}`);

    if(!res.ok){
        alert("회사 위치를 찾을 수 없습니다.2");
        return;
    }

    const data = await res.json();

    document.getElementById("company_id").value = data.company_id;
    document.getElementById("company_name").value = data.company_name;
    document.getElementById("loc_code").value = data.loc_code;
    document.getElementById("lat").value = data.lat;
    document.getElementById("lng").value = data.lng;
    document.getElementById("accuracy").value = data.accuracy;
    document.getElementById("remark").value = data.remark;
    document.getElementById("use_yn").value = data.use_yn;

}

/********************************************************
 * 수정 저장
 ********************************************************/
async function saveUpdateLocation() {
    const company_id = (document.getElementById("company_id").value || "").trim();
    const company_name = (document.getElementById("company_name").value || "").trim();
    const loc_code = (document.getElementById("loc_code").value || "").trim();
    const lat = parseFloat(document.getElementById("lat").value);
    const lng = parseFloat(document.getElementById("lng").value);
    const accuracy = parseFloat(document.getElementById("accuracy").value);
    const remark = document.getElementById("remark").value;
    const use_yn = document.getElementById("use_yn").value;


    if (!/^[0-9]+$/.test(accuracy)) {
        alert("정확도는 숫자만 가능합니다.");
        document.getElementById("accuracy").focus();
        return;
    }

    if (!/^-?\d+(\.\d+)?$/.test(lat)) {
        alert("위도는 정수, 소수점 포함 숫자만 가능합니다.");
        document.getElementById("lat").focus();
        return;
    }
    if (!/^-?\d+(\.\d+)?$/.test(lng)) {
        alert("경도는 정수, 소수점 포함 숫자만 가능합니다.");
        document.getElementById("lng").focus();
        return;
    }

    if(lat < -90 || lat > 90 || lng < -180 || lng > 180){
        alert("위도는 -90~90, 경도는 -180~180 범위여야 합니다.");
        return;
    }

    const data = {
        company_name: company_name,
        lat: Number.isNaN(lat) ? 0 : lat,
        lng: Number.isNaN(lng) ? 0 : lng,
        accuracy: Number.isNaN(accuracy) ? 0 : accuracy,
        remark: remark || "",
        use_yn: use_yn
    };


    try{
        const response = await fetch(`/location/${encodeURIComponent(company_id)}/${encodeURIComponent(loc_code)}`, {
            method: "PUT",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        });
        if(response.ok){
            alert("수정되었습니다.");
            location.href="/web/location/locList.html";
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


/**************************************************************************
 * PopUp(location_popup.js)
 **************************************************************************/

async function loadLocationPopup(){
    const company_name = document.getElementById("search_name").value;
    const response =
        await fetch(
            "/location/list?company_name="
            + encodeURIComponent(company_name)
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
            <td>${d.company_id}</td>
            <td>${d.company_name}</td>
            <td>${d.loc_code}</td>
            <td>${d.lat}</td>
            <td>${d.lng}</td>
            <td>${d.remark}</td>
            <td align='center'>
                <button onclick="selectLocation('${d.company_id}','${d.loc_code}','${d.company_name}')">선택</button>
            </td>
        </tr>
        `;
    });

    tbody.innerHTML = html;
}

function selectLocation(id,cd,name){
    window.opener.setParentLocation(id,cd,name);
    window.close();
}

/*************************************************
 * 부모부서 찾기
 *************************************************/
function popupLocation(){
    window.open(
        "/web/location/locpopup.html",
        "location",
        "width=650,height=420"
    );
}


/*************************************************
 * 부모부서 선택
 *************************************************/
function setParentLocation(id,cd,name){
    document.getElementById("parent_id").value=id;
    document.getElementById("parent_cd").value=cd;
    document.getElementById("parent_name").value=name;
}