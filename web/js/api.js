const Api = {

    async get(url){

        Loading.show();

        try{

            const res = await fetch(url,{
                headers:{
                    "Authorization":"Bearer "+getToken()
                }
            });

            if(res.status==401){

                Dialog.alert("로그인이 만료되었습니다.");

                logout();

                return;

            }

            return await res.json();

        }
        finally{

            Loading.hide();

        }

    },

    async post(url,data){

        Loading.show();

        try{

            const res = await fetch(url,{

                method:"POST",

                headers:{

                    "Content-Type":"application/json",

                    "Authorization":"Bearer "+getToken()

                },

                body:JSON.stringify(data)

            });

            if(res.status==401){

                Dialog.alert("로그인이 만료되었습니다.");

                logout();

                return;

            }

            return await res.json();

        }
        finally{

            Loading.hide();

        }

    },

    async put(url,data){

        Loading.show();

        try{

            const res = await fetch(url,{

                method:"PUT",

                headers:{

                    "Content-Type":"application/json",

                    "Authorization":"Bearer "+getToken()

                },

                body:JSON.stringify(data)

            });

            return await res.json();

        }
        finally{

            Loading.hide();

        }

    },

    async delete(url){

        Loading.show();

        try{

            const res=await fetch(url,{

                method:"DELETE",

                headers:{
                    "Authorization":"Bearer "+getToken()
                }

            });

            return await res.json();

        }
        finally{

            Loading.hide();

        }

    }

};