const Grid={

    async load(option){

        const table=document.querySelector(option.table);

        table.innerHTML="";

        //-------------------------
        // Header
        //-------------------------

        let thead=table.createTHead();

        let row=thead.insertRow();

        if(option.checkbox){

            row.innerHTML+="<th width='40'><input type='checkbox' id='chkAll'></th>";

        }

        option.columns.forEach(c=>{

            row.innerHTML+=`
                <th style="width:${c.width||150}px">
                    ${c.title}
                </th>
            `;

        });

        //-------------------------
        // Data
        //-------------------------

        const data=await Api.get(option.url);

        let tbody=table.createTBody();

        data.forEach(item=>{

            let r=tbody.insertRow();

            if(option.checkbox){

                r.innerHTML+=`
                    <td align="center">

                        <input type="checkbox"
                            class="grid-check">

                    </td>
                `;

            }

            option.columns.forEach(col=>{

                r.innerHTML+=`

                    <td>

                        ${item[col.field]??""}

                    </td>

                `;

            });

            //--------------------
            // Double Click
            //--------------------

            if(option.dblclick){

                r.ondblclick=function(){

                    option.dblclick(item);

                }

            }

        });

        //-------------------------
        // Select All
        //-------------------------

        if(option.checkbox){

            document.getElementById("chkAll").onclick=function(){

                document.querySelectorAll(".grid-check")

                    .forEach(c=>{

                        c.checked=this.checked;

                    });

            };

        }

    }

}

function badge(value){
    switch(value){
        case "PENDING":
            return "<span class='badge badge-warning'>승인대기</span>";
        case "APPROVED":
            return "<span class='badge badge-success'>승인</span>";
        case "REJECTED":
            return "<span class='badge badge-danger'>거부</span>";
        default:
            return value;
    }
}

class Grid{
    constructor(id){
        this.table=document.getElementById(id);
        this.data=[];
    }

    setData(data){
        this.data=data;
        this.render();
    }

    render(){
    }
}

selectRow(tr){
    this.table
        .querySelectorAll("tbody tr")
        .forEach(r=>r.classList.remove("grid-row-selected"));

    tr.classList.add("grid-row-selected");
}