/**************************************************************************
 * HR_SYSTEM
 * Grid Framework v1.0.0
 * grid.js
 **************************************************************************/

class Grid{
    constructor(option){
        this.option = Object.assign({
            table:null,
            columns:[],
            pageSize:20,
            rowNumber:false,
            checkBox:false,
            sortable:true,
            paging:true,
            emptyMessage:"조회된 데이터가 없습니다.",
            onClick:null,
            onDoubleClick:null
        },option);

        this.table=document.querySelector(this.option.table);

        if(!this.table){
            throw new Error("Grid Table Not Found.");
        }

        this.thead=this.table.querySelector("thead");
        this.tbody=this.table.querySelector("tbody");
        this.data=[];
        this.view=[];
        this.selectedIndex=-1;
        this.sortField=null;
        this.sortAsc=true;
        this.loading=false;
        this.init();
    }

    /********************************************************
     * 초기화
     ********************************************************/
    init(){
        this.createHeader();
        this.renderEmpty();
    }

    /********************************************************
     * Header 생성
     ********************************************************/
    createHeader(){
        this.thead.innerHTML="";
        const tr=document.createElement("tr");

        if(this.option.checkBox){
            const th=document.createElement("th");

            th.style.width="40px";
            th.innerHTML=
            "<input type='checkbox' class='grid-check-all'>";
            tr.appendChild(th);
        }

        if(this.option.rowNumber){
            const th=document.createElement("th");

            th.style.width="60px";
            th.innerHTML="No";
            tr.appendChild(th);
        }

        this.option.columns.forEach(col=>{
            const th=document.createElement("th");
            th.innerHTML=col.title;
            if(col.width){
                th.style.width=col.width+"px";
            }

            if(this.option.sortable){
                th.style.cursor="pointer";
                th.onclick=()=>{
                    this.sort(col.field);
                };
            }
            tr.appendChild(th);
        });

        this.thead.appendChild(tr);
    }

    /********************************************************
     * 데이터 설정
     ********************************************************/
    setData(data){
        this.data=data||[];
        this.view=[...this.data];
        this.render();
    }

    /********************************************************
     * 다시그리기
     ********************************************************/
    refresh(){
        this.render();
    }

    /********************************************************
     * Render
     ********************************************************/
    render(){
        this.renderBody();
    }

    /********************************************************
     * Body
     ********************************************************/
    renderBody(){
        this.tbody.innerHTML="";
        if(this.view.length===0){
            this.renderEmpty();
            return;
        }

        this.view.forEach((row,index)=>{
            const tr=document.createElement("tr");

            tr.dataset.index=index;
            tr.onclick=()=>{
                this.select(index);
            };

            tr.ondblclick=()=>{
                if(this.option.onDoubleClick){
                    this.option.onDoubleClick(row);
                }
            };

            if(this.option.checkBox){
                const td=document.createElement("td");

                td.innerHTML=
                "<input type='checkbox' class='grid-check'>";

                tr.appendChild(td);

            }

            if(this.option.rowNumber){
                const td=document.createElement("td");
                td.innerHTML=index+1;
                tr.appendChild(td);
            }

            this.option.columns.forEach(col=>{
                const td=document.createElement("td");
                let value=row[col.field];
                if(value==null){
                    value="";
                }
                td.innerHTML=value;
                tr.appendChild(td);
            });
            this.tbody.appendChild(tr);
        });
    }

    /********************************************************
     * 선택
     ********************************************************/
    select(index){
        this.selectedIndex=index;
        this.tbody
            .querySelectorAll("tr")
            .forEach(r=>{
                r.classList.remove("grid-selected");
            });
        const row=this.tbody.rows[index];
        if(row){
            row.classList.add("grid-selected");
        }

        if(this.option.onClick){
            this.option.onClick(this.view[index]);
        }
    }

    /********************************************************
     * 선택 데이터
     ********************************************************/
    getSelected(){
        if(this.selectedIndex<0){
            return null;
        }
        return this.view[this.selectedIndex];
    }

    /********************************************************
     * Empty
     ********************************************************/
    renderEmpty(){
        const colspan=
            this.option.columns.length
            +(this.option.rowNumber?1:0)
            +(this.option.checkBox?1:0);

        this.tbody.innerHTML=
        `<tr>
            <td colspan="${colspan}">
                <div class="grid-empty">
                    ${this.option.emptyMessage}
                </div>
            </td>
        </tr>`;

    }

    /********************************************************
     * Loading
     ********************************************************/
    showLoading(){
        let loading=
            document.querySelector(".grid-loading");

        if(loading){
            loading.classList.add("show");
        }
    }

    hideLoading(){
        let loading=
            document.querySelector(".grid-loading");

        if(loading){
            loading.classList.remove("show");
        }
    }

    /********************************************************
     * 정렬 (Release2)
     ********************************************************/
    sort(field){
        console.log(field);
    }

    /********************************************************
    * Sort
    ********************************************************/
    sort(field){
        if(this.sortField===field){
            this.sortAsc=!this.sortAsc;
        }else{
            this.sortField=field;
            this.sortAsc=true;
        }
        this.view.sort((a,b)=>{        
            let v1=a[field];
            let v2=b[field];

            if(v1==null) v1="";
            if(v2==null) v2="";

        if(typeof v1==="number"){
            return this.sortAsc
                ? v1-v2
                : v2-v1;
        }

        v1=v1.toString();
        v2=v2.toString();

        return this.sortAsc
            ? v1.localeCompare(v2)
            : v2.localeCompare(v1);
        });
        this.renderBody();
    }

    /********************************************************
    * Formatter
    ********************************************************/
    format(col,value,row){
        if(col.formatter){
            return col.formatter(value,row);
        }
        return value ?? "";
    }

    /********************************************************
    * Badge Formatter
    ********************************************************/
    badge(text,color){
        return `  <span class="grid-badge grid-badge-${color}">
            ${text}  </span>
        `;
    }

    /********************************************************
    * Number Formatter
    ********************************************************/
    number(value){
        if(value==null) return "";
            return Number(value).toLocaleString();
    }

    /********************************************************
    * Date Formatter
    ********************************************************/
    date(value){
        if(!value) return "";
            return value.substring(0,10);
    }

    /********************************************************
    * Footer
    ********************************************************/
    renderFooter(){
        if(!this.option.footer){
            return;
    }

    let footer=document.querySelector(".grid-total");

    if(!footer){
        return;
    }

    footer.innerHTML=
    "총 "+this.view.length.toLocaleString()+" 건";
    }

    /********************************************************
    * 전체선택
    ********************************************************/
    checkAll(flag){
        this.tbody.querySelectorAll(".grid-check")
        .forEach(chk=>{
            chk.checked=flag;
        });
    }

    /********************************************************
    * 선택데이터
    ********************************************************/
    getChecked(){
        const rows=[];
        
        this.tbody.querySelectorAll("tr").forEach((tr,index)=>{
            const chk=tr.querySelector(".grid-check");

            if(chk && chk.checked){
                rows.push(this.view[index]);
            }
        });
        return rows;
    }

    /********************************************************
    * Column Resize
    ********************************************************/
    enableResize(){
        const headers=this.thead.querySelectorAll("th");
        headers.forEach(th=>{
            const resizer=document.createElement("div");
            resizer.className="grid-resizer";

            th.appendChild(resizer);

            let startX=0;
            let startWidth=0;

            resizer.onmousedown=(e)=>{
                startX=e.pageX;
                startWidth=th.offsetWidth;
                document.onmousemove=(ev)=>{
                    th.style.width=
                        (startWidth+(ev.pageX-startX))+"px";
                };

                document.onmouseup=()=>{
                    document.onmousemove=null;
                    document.onmouseup=null;
                };
            };
        });
    }

    /********************************************************
    * Filter
    ********************************************************/
    filter(keyword){
        if(!keyword){
            this.view=[...this.data];
            this.renderBody();
            return;
        }

        keyword=keyword.toLowerCase();

        this.view=this.data.filter(row=>{
            for(let key in row){
                if(row[key]==null) continue;
                if(row[key]
                    .toString()
                    .toLowerCase()
                    .includes(keyword))
                    return true;
                }
                return false;
            });
            
        this.renderBody();
    }

    /********************************************************
    * Context Menu
    ********************************************************/
    enableContextMenu(){
        this.tbody.oncontextmenu=(e)=>{
            e.preventDefault();
            const menu=document.querySelector(".grid-menu");

            if(!menu) return;

            menu.style.left=e.pageX+"px";
            menu.style.top=e.pageY+"px";
            menu.style.display="block";
        };

        document.onclick=()=>{
            const menu=document.querySelector(".grid-menu");
            if(menu){
                menu.style.display="none";
            }
        };
    }

    /********************************************************
    * Keyboard Navigation
    ********************************************************/
    enableKeyboard(){
        document.onkeydown=(e)=>{
        if(this.selectedIndex<0) return;

        switch(e.key){
            case "ArrowDown":
                if(this.selectedIndex<this.view.length-1){
                    this.select(this.selectedIndex+1);
                }
                break;

            case "ArrowUp":
                if(this.selectedIndex>0){
                    this.select(this.selectedIndex-1);
                }
                break;
            }
        };
    }

    /********************************************************
    * Highlight
    ********************************************************/
    highlight(text){
        if(!text) return;
        this.tbody.querySelectorAll("td")
        .forEach(td=>{
            td.innerHTML=td.innerHTML.replaceAll(
                text,
                "<span class='grid-highlight'>"+text+"</span>"
            );
        });
    }

    /********************************************************
    * Excel Export
    ********************************************************/
    exportExcel(){
        console.log("Excel Export");
    }

    /********************************************************
    * Print
    ********************************************************/
    print(){
        window.print();
    }

}

