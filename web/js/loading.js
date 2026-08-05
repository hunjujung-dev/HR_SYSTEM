const Loading={

    show(){

        if(document.getElementById("loading")) return;

        const div=document.createElement("div");

        div.id="loading";

        div.innerHTML=`

            <div class="loading-box">

                <div class="spinner"></div>

                <div>

                    처리중입니다...

                </div>

            </div>

        `;

        document.body.appendChild(div);

    },

    hide(){

        const div=document.getElementById("loading");

        if(div)

            div.remove();

    }

}