/**************************************************************************
 * department_tree.js
 * Department Tree
 **************************************************************************/

let treeData = [];
let selectedDept = "";

/********************************************************
 * Tree 조회
 ********************************************************/
async function loadDepartmentTree(){
    try{
        const response = await fetch("/department/tree");
        if(!response.ok){
            alert("부서 Tree 조회 실패");
            return;
        }

        treeData = await response.json();

        drawDepartmentTree(treeData);
        enableTreeDrag();
    }
    catch(e){
        console.error(e);
        alert("Tree 조회 실패");
    }
}


/********************************************************
 * Tree 생성
 ********************************************************/
function drawDepartmentTree(data){

    const tree = document.getElementById("deptTree");

    console.log(tree);

    if(tree==null){
        return;
    }
    tree.innerHTML="";

    const ul=document.createElement("ul");

    ul.className="tree-root";

    data.forEach(node=>{
        ul.appendChild(
            createTreeNode(node)
        );
    });

    tree.appendChild(ul);
}


/********************************************************
 * Node 생성
 ********************************************************/
function createTreeNode(node){
    const li=document.createElement("li");

    li.className="tree-node";
    li.dataset.dept=node.dept_cd;

    //--------------------------------------------------
    const row=document.createElement("div");

    row.className="tree-row";
    //--------------------------------------------------
    const toggle=document.createElement("span");

    toggle.className="tree-toggle";
    //--------------------------------------------------

    if(node.children.length>0){
        toggle.innerHTML='<i class="fa-solid fa-caret-right"></i>';   // 접힘
    }
    else{
        toggle.innerHTML="";
    }

    //--------------------------------------------------
    toggle.onclick=function(e){
        e.stopPropagation();
        toggleTree(li);
    };
    //--------------------------------------------------
    const icon=document.createElement("span");

    icon.className="tree-icon";
    icon.innerHTML="📁";
    //--------------------------------------------------
    const text=document.createElement("span");

    text.className="tree-text";
    text.innerHTML=node.dept_name;
    //--------------------------------------------------
    row.appendChild(toggle);
    row.appendChild(icon);
    row.appendChild(text);
    //--------------------------------------------------

    row.onclick=function(){
        selectDepartment(node.dept_cd,row);
    };

    //--------------------------------------------------
    li.appendChild(row);
    //--------------------------------------------------

    if(node.children.length>0){

        const child=document.createElement("ul");

        child.style.display="none";
        node.children.forEach(c=>{
            child.appendChild(
                createTreeNode(c)
            );
        });
        li.appendChild(child);
    }

    return li;
}

/**************************************************************************
 * Tree 펼치기 / 접기
 **************************************************************************/
function toggleTree(li){
    const child = li.querySelector(":scope > ul");

    if(child==null){
        return;
    }

    const toggle =
        li.querySelector(":scope > .tree-row > .tree-toggle");

    const icon =
        li.querySelector(":scope > .tree-row > .tree-icon");

    if(child.style.display=="none"){
        child.style.display="block";
        toggle.innerHTML='<i class="fa-solid fa-caret-down"></i>';   // 펼침
        icon.innerHTML='<i class="fa-regular fa-folder-open"></i>';    // 펼침
    }
    else{
        child.style.display="none";
        toggle.innerHTML='<i class="fa-solid fa-caret-right"></i>';   // 접힘
        icon.innerHTML='<i class="fa-regular fa-folder"></i>';  // 접힘
    }
}


/**************************************************************************
 * Tree 선택
 **************************************************************************/
function selectDepartment(dept_cd,row){

    selectedDept=dept_cd;

    //------------------------------------
    document
        .querySelectorAll(".tree-row")
        .forEach(r=>{
            r.classList.remove("tree-selected");
        });

    //------------------------------------
    row.classList.add("tree-selected");
    //------------------------------------

    loadDepartmentGrid(dept_cd);
}


/**************************************************************************
 * Grid 조회
 **************************************************************************/
function loadDepartmentGrid(dept_cd){
    const url =
        "/department/list"
        + "?dept_cd="
        + encodeURIComponent(dept_cd);
    fetch(url)
        .then(res=>res.json())
        .then(data=>{
            departmentList = data;
            if(typeof drawDepartment === "function"){
                drawDepartment(data);
            }
        })
        .catch(console.error);
}


/**************************************************************************
 * Tree Refresh
 **************************************************************************/
function refreshDepartmentTree(){
    loadDepartmentTree();
}


/**************************************************************************
 * 선택 부서
 **************************************************************************/
function getSelectedDepartment(){
    return selectedDept;
}


/**************************************************************************
 * Tree 전체 펼치기
 **************************************************************************/
function expandAll(){
    document
        .querySelectorAll("#deptTree ul")
        .forEach(ul=>{
            ul.style.display="block";
        });

    document
        .querySelectorAll(".tree-toggle")
        .forEach(t=>{
            if(t.innerHTML!=""){
                t.innerHTML="▼";
            }
        });

    document
        .querySelectorAll(".tree-icon")
        .forEach(i=>{
            i.innerHTML="📂";
        });
}


/**************************************************************************
 * Tree 전체 접기
 **************************************************************************/
function collapseAll(){
    document
        .querySelectorAll("#deptTree ul")
        .forEach((ul,index)=>{
            if(index>0){
                ul.style.display="none";
            }
        });

    document
        .querySelectorAll(".tree-toggle")
        .forEach(t=>{
            if(t.innerHTML!=""){
                t.innerHTML="▶";
            }
        });

    document
        .querySelectorAll(".tree-icon")
        .forEach(i=>{
            i.innerHTML="📁";
        });
}


/**************************************************************************
 * 초기 실행
 **************************************************************************/
document.addEventListener(
    "DOMContentLoaded",
    function(){
        loadDepartmentTree();
    }
);

/**************************************************************************
 * Drag & Drop
 **************************************************************************/

let dragNode = null;
let dropNode = null;

/********************************************************
 * Drag 적용
 ********************************************************/
function enableTreeDrag() {
    document.querySelectorAll(".tree-row").forEach(row => {
        row.draggable = true;
        row.ondragstart = dragStart;
        row.ondragover = dragOver;
        row.ondrop = dropTree;
        row.ondragend = dragEnd;
    });
}

/********************************************************
 * Drag Start
 ********************************************************/
function dragStart(e) {
    dragNode = this.parentElement;
    this.classList.add("tree-drag");
}

/********************************************************
 * Drag Over
 ********************************************************/
function dragOver(e) {
    e.preventDefault();
}

/********************************************************
 * Drop
 ********************************************************/
function dropTree(e) {
    e.preventDefault();

    dropNode = this.parentElement;

    if (dragNode == dropNode)
        return;

    const dragDept = dragNode.dataset.dept;
    const targetDept = dropNode.dataset.dept;

    moveDepartment(
        dragDept,
        targetDept
    );
}

/********************************************************
 * Drag End
 ********************************************************/
function dragEnd() {
    document
        .querySelectorAll(".tree-row")
        .forEach(r => {
            r.classList.remove("tree-drag");
        });
}

/**************************************************************************
 * 부서 이동
 **************************************************************************/
async function moveDepartment(
    dept_cd,
    target_cd
){

    if(!confirm("부서를 이동하시겠습니까?")){
        return;
    }

    const response =
        await fetch(
            "/department/move",
            {
                method:"PUT",
                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({
                    dept_cd:dept_cd,
                    parent_cd:target_cd
                })
            }
        );
    if(response.ok){
        loadDepartmentTree();
        if(selectedDept){
            loadDepartmentGrid(selectedDept);
        }
    }
    else{
        alert("이동 실패");
    }
}

/**************************************************************************
 * Sort 저장
 **************************************************************************/
async function saveSort(){

    const rows=[];

    document
        .querySelectorAll(".tree-node")
        .forEach((node,index)=>{
            rows.push({
                dept_cd:node.dataset.dept,
                sort_no:index+1
            });
        });

    await fetch(
        "/department/sort",
        {
            method:"PUT",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify(rows)
        }
    );
}


/**************************************************************************
 * 우클릭 메뉴
 **************************************************************************/
document.addEventListener("contextmenu",function(e){

    const row=e.target.closest(".tree-row");

    if(!row){

        return;

    }

    e.preventDefault();

    selectedDept=row.parentElement.dataset.dept;

    showTreeMenu(
        e.pageX,
        e.pageY
    );

});

/**************************************************************************
 * 메뉴생성
 **************************************************************************/
function showTreeMenu(x,y){

    const menu=document.getElementById("treeMenu");

    menu.style.left=x+"px";

    menu.style.top=y+"px";

    menu.style.display="block";

}

document.onclick=function(){

    document.getElementById("treeMenu").style.display="none";

}

/**************************************************************************
 * 메뉴연결
 **************************************************************************/

function treeAdd(){

    location.href=
        "/web/emplopyee/deptadd.html?parent="+selectedDept;

}

function treeEdit(){

    location.href=
        "/web/emplopyee/deptedit.html?id="+selectedDept;

}

function treeDelete(){

    departmentDelete(selectedDept);

}