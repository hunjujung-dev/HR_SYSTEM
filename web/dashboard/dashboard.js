let attendanceChart = null;
let deptChart = null;
let dashboardLoaded = false;

window.onload = async function(){

    await loadLayout();
    await loadDashboard();
};

async function loadDashboard(){

    if (dashboardLoaded) {
        return;
    }

    const d = await Api.get("/dashboard");

    // 카드 값
    document.getElementById("empCount").innerText = d.employee_count;
    document.getElementById("checkIn").innerText = d.checkin_count;
    document.getElementById("checkOut").innerText = d.checkout_count;
    document.getElementById("pending").innerText = d.pending_device;
    document.getElementById("gps").innerText = d.gps_company;
    document.getElementById("todayWork").innerText = d.today_work;

    // 최근 출근
    const recent = document.getElementById("recentCheckin");
    recent.innerHTML = "";

    d.recent_checkin.forEach(r => {
        recent.innerHTML += `<li>${r.time} ${r.name}</li>`;
    });

    // 공지사항
    const notice = document.getElementById("noticeList");
    notice.innerHTML = "";

    d.notice.forEach(n => {
        notice.innerHTML += `<li>${n.title}</li>`;
    });

    drawAttendanceChart(d.attendance_chart);
    drawDeptChart(d.dept_chart);
    dashboardLoaded = true;
}

function drawAttendanceChart(data){

    const ctx = document.getElementById("attendanceChart");

    if (!ctx) {
        return;
    }

    const labels = Array.isArray(data.labels) ? data.labels : [];
    const values = Array.isArray(data.values)
        ? data.values.map(v => {
            const n = Number(v);
            return Number.isFinite(n) ? Math.round(n) : 0;
        })
        : [];

    if (attendanceChart) {
        attendanceChart.destroy();
    }

    attendanceChart = new Chart(ctx,{ 
        type:"bar",
        data:{
            labels: labels,
            datasets:[{
                label:"인원",
                data: values,
                backgroundColor:[
                    "#1191D0",
                    "#27AE60",
                    "#F2C94C",
                    "#EB5757"
                ]
            }]
        }
        /*
        * 옵션 진행 시 화면이 길게 늘어짐
        ,
        options:{
            responsive:true,
            maintainAspectRatio:false,
            scales:{
                y:{
                    beginAtZero:true,
                    ticks:{
                        precision:0,
                        stepSize:1,
                        callback:(value) => Number.isInteger(value) ? value : null
                    }
                }
            },
            plugins:{
                tooltip:{
                    callbacks:{
                        label:(context) => `${context.dataset.label}: ${Math.round(context.parsed.y)}`
                    }
                }
            }
        }
        */
    });
}

function drawDeptChart(data){

    const ctx = document.getElementById("deptChart");

    if (deptChart) {
        deptChart.destroy();
    }

    deptChart = new Chart(ctx,{
        type:"doughnut",
        data:{
            labels:data.labels,
            datasets:[{
                data:data.values,
                backgroundColor:[
                    "#1191D0",
                    "#27AE60",
                    "#F2C94C",
                    "#EB5757",
                    "#9B51E0"
                ]
            }]
        }
        /*
        * 옵션 진행 시 화면이 길게 늘어짐
        ,
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
        */
    });
}