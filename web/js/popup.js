const Popup={

    callback:null,

    open(option){

        this.callback=option.callback;

        const w=window.open(
            option.url,
            "_blank",
            `width=${option.width},
             height=${option.height},
             resizable=yes`
        );

        w.focus();

    },

    close(){

        window.close();

    },

    success(){

        if(window.opener){

            if(Popup.callback){

                Popup.callback();

            }

            window.close();

        }

    }

}