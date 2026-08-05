class Tree{
    constructor(option){
        this.option = Object.assign({
            target:null,
            childrenField:"children",
            idField:"id",
            textField:"text",
            parentField:"parent",
            expand:true,
            onClick:null,
            onContextMenu:null
        },option);
        this.container=document.querySelector(this.option.target);
        this.data=[];
        this.selectedNode=null;
    }

    setData(data){
        this.data=data||[];
        this.render();
    }

    render(){
        this.container.innerHTML="";
        const ul=document.createElement("ul");
        ul.className="tree-root";
        this.data.forEach(node=>{
            ul.appendChild(this.createNode(node));
        });
        this.container.appendChild(ul);
    }

    createNode(node){
        const li=document.createElement("li");
        const row=document.createElement("div");
        row.className="tree-row";
        row.innerHTML=`
            <span class="tree-toggle">
                ${node.children?.length?"▼":""}
            </span>
            <span class="tree-icon">
                📁
            </span>
            <span class="tree-text">
                ${node[this.option.textField]}
            </span>
        `;
        row.onclick=()=>{
            this.select(node,row);
        };
        li.appendChild(row);
        if(node.children && node.children.length){
            const ul=document.createElement("ul");
            node.children.forEach(child=>{
                ul.appendChild(this.createNode(child));
            });
            li.appendChild(ul);
        }
        return li;
    }

    select(node,row){
        this.container
            .querySelectorAll(".tree-selected")
            .forEach(r=>{
                r.classList.remove("tree-selected");
            });
        row.classList.add("tree-selected");
        this.selectedNode=node;
        if(this.option.onClick){
            this.option.onClick(node);
        }
    }

    toggle(row){

        const ul=row.parentElement.querySelector("ul");
        if(!ul) return;
        const icon=row.querySelector(".tree-toggle");
        if(ul.style.display==="none"){
            ul.style.display="block";
            icon.innerHTML="▼";
        }else{
            ul.style.display="none";
            icon.innerHTML="▶";
        }
    }

    search(keyword){
        keyword=keyword.toLowerCase();

        this.container
            .querySelectorAll(".tree-row")
            .forEach(row=>{
                const text=row
                    .querySelector(".tree-text")
                    .innerText
                    .toLowerCase();
                row.parentElement.style.display=
                    text.includes(keyword)
                        ?"block":"none";
            });
    }

    enableDrag(){
        this.container
            .querySelectorAll("ul")
            .forEach(ul=>{
                Sortable.create(ul,{
                    animation:150,
                    group:"tree",
                    fallbackOnBody:true,
                    swapThreshold:.65,
                    onEnd:(evt)=>{
                        this.saveOrder(evt);
                    }
                });
            });
    }

    saveOrder(evt){
        if(!this.option.onDrop){
            return;
        }

        this.option.onDrop({
            parent:this.getParent(evt.to),
            from:evt.oldIndex,
            to:evt.newIndex
        });
    }

    find(id){
        return this.findRecursive(
            this.data,
            id
        );
    }

    findRecursive(list,id){
        for(let n of list){
            if(n[this.option.idField]==id){
                return n;
            }
            if(n.children){
                let r=this.findRecursive(
                    n.children,
                    id
                );

                if(r){
                    return r;
                }
            }
        }
        return null;
    }

    append(parentId,node){
        let p=this.find(parentId);
        if(!p){
            this.data.push(node);
        }else{
            if(!p.children){
                p.children=[];
            }
            p.children.push(node);
        }
        this.render();
    }

    remove(id){
        this.removeRecursive(
            this.data,
            id
        );
        this.render();
    }

    removeRecursive(list,id){
        for(let i=0;i<list.length;i++){
            if(list[i][this.option.idField]==id){
                list.splice(i,1);
                return true;
            }

            if(list[i].children){
                if(
                    this.removeRecursive(
                        list[i].children,
                        id
                    )
                ){
                    return true;
                }
            }
        }
    }

    update(id,data){
        let node=this.find(id);
        if(!node) return;
        Object.assign(node,data);
        this.render();
    }

    refresh(){
        this.render();
    }

    saveExpand(){
        let ids=[];
        this.container
            .querySelectorAll("li")
            .forEach(li=>{
                if(
                    li.classList.contains("tree-open")
                ){
                    ids.push(
                        li.dataset.id
                    );
                }
            });

        localStorage.setItem(
            "TREE_EXPAND",
            JSON.stringify(ids)
        );
    }

    restoreExpand(){
        let ids=JSON.parse(
            localStorage.getItem(
                "TREE_EXPAND"
            )||"[]"
        );

        ids.forEach(id=>{
            let li=this.container.querySelector(
                "[data-id='"+id+"']"
            );

            if(li){
                li.classList.add(
                    "tree-open"
                );
            }
        });
    }

    changeFolder(row,open){
        let icon=row.querySelector(".tree-icon");
        icon.innerHTML=open?
        "📂":"📁";
    }

}