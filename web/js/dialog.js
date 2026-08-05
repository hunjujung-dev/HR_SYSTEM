const Dialog={

    alert(msg){

        const bg=document.createElement("div");

        bg.className="dialog-bg";

        bg.innerHTML=`
            <div class="dialog">

                <div class="dialog-title">
                    알림
                </div>

                <div class="dialog-body">

                    ${msg}

                </div>

                <div class="dialog-footer">

                    <button class="btn" id="btnOk">

                        확인

                    </button>

                </div>

            </div>
        `;

        document.body.appendChild(bg);

        document.getElementById("btnOk").onclick=function(){

            bg.remove();

        };

    },

    confirm(msg,callback){

        const bg=document.createElement("div");

        bg.className="dialog-bg";

        bg.innerHTML=`

        <div class="dialog">

            <div class="dialog-title">

                확인

            </div>

            <div class="dialog-body">

                ${msg}

            </div>

            <div class="dialog-footer">

                <button class="btn"

                    id="btnCancel">

                    취소

                </button>

                <button class="btn btn-primary"

                    id="btnYes">

                    확인

                </button>

            </div>

        </div>

        `;

        document.body.appendChild(bg);

        btnCancel.onclick=()=>bg.remove();

        btnYes.onclick=()=>{

            bg.remove();

            callback();

        };

    }

}