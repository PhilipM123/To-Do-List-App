document.addEventListener('DOMContentLoaded', function(){

    // Edit List page
    const newListDiv = document.querySelector("#new-list-item");
    if(newListDiv){
        const form = newListDiv.querySelector("#newItem");
        const listItems = newListDiv.querySelector(".listItems");
    
        form.onsubmit = function(e){
            e.preventDefault();
    
            const nameEl = e.target.querySelector("input[name=content]");
    
            if (nameEl.value){

                const elemDiv = document.createElement("div");
                elemDiv.className = "flex justify-between select-none cursor-pointer border-t-2 border-gray border-opacity-0  bg-white mb-1 rounded-md p-2 transition duration-500 ease-in-out hover:-translate-y-1 hover:shadow-lg hover:border-opacity-100";
            
                const elem = document.createElement("li");
                elem.innerHTML = nameEl.value;
                elem.className = "font-semibold block text-s text-black";
                elemDiv.appendChild(elem);
                console.log(elemDiv);

                listItems.insertAdjacentHTML("afterbegin", 
                `<div class="flex justify-between select-none cursor-pointer border-t-2 border-gray border-opacity-0  bg-white mb-1 rounded-md p-2 transition duration-500 ease-in-out hover:-translate-y-1 hover:shadow-lg hover:border-opacity-100">
                <li class="font-semibold block text-s text-black">${nameEl.value}</li>
                </div>`
                );
            
                id = newListDiv.querySelector("*[name=id]").value;
                const data = new FormData(e.target);
                const values = Object.fromEntries(data);
        
                const content = nameEl.value;
                const body = {content};
        
                const response = fetch(`/create_list_item/${id}`, {
                    method : "POST",
                    headers: {
                        "X-CSRFToken": values.csrfmiddlewaretoken
                    },
                    body : JSON.stringify(body)
                })
                nameEl.value = "";
            } else{
                alert("please enter a new list item");
            };
        };
    };

    // Delete List 
    const deleteListForm = document.querySelectorAll("form[name=deleteListForm]");

    
    if(deleteListForm){
        deleteListForm.forEach(form =>{
            form.addEventListener("submit", function(e){
                e.preventDefault();
                const listId = e.target.querySelector("input[name=deleteListId]").value;
                const list = e.target.parentNode;
                const listitems = list.querySelectorAll(".listitem"); //listitem doesn't exist anymore
                const data = new FormData(e.target);
                const values = Object.fromEntries(data);

                const P1 = form.parentElement;
                const totalListDiv = P1.parentElement;

                totalListDiv.innerHTML = "";
                totalListDiv.className = "flex justify-center shadow-xl w-4/12 shadow-md rounded px-4 pt-4 pb-4 mb-4 bg-white text-l text-black font-semibold";
                totalListDiv.innerHTML = "List has been deleted";
                
                const response = fetch(`/delete_list/${listId}`, {
                    method : "POST",
                    headers: {
                        "X-CSRFToken": values.csrfmiddlewaretoken
                    },
                });
    
                listitems.forEach(el => {
                    el.innerHTML = "";
                });
                var heading = document.createElement("h6");
                heading.innerHTML = "list has been deleted";
                heading.setAttribute("class","font-semibold block text-l font-bold text-white");
                list.appendChild(heading);
            });
        });
    };


    // Follow Lists
    const followListForm = document.querySelectorAll("form[name=followListForm]");
    
    if(followListForm){
        followListForm.forEach(form =>{
           
            //Set btn to Follow/Un-Follow
            const followBtn = form.querySelector("input[name=followBtn]");
            const followListId = form.querySelector("input[name=followListId]").value;
            
            
    
            const getFollowResponse = fetch(`/get_follow/${followListId}`, {
                method : "GET",
            }).then(response => response.json()).then(data =>{
                var followBool = data.data;
                if(followBool){
                    followBtn.value = "Un-Follow";
                } else{
                    followBtn.value = "Follow";
                }
            });
    
            form.addEventListener("submit", function(e){
                e.preventDefault();
                const listId = e.target.querySelector("input[name=followListId]").value;
                const data = new FormData(e.target);
                const values = Object.fromEntries(data);
    
                const response = fetch(`/follow_list/${listId}`,{
                    method : "POST",
                    headers: {
                        "X-CSRFToken": values.csrfmiddlewaretoken
                    },
                }).then(response => response.json()).then(data =>{
                    var followBool = data.data;
                    console.log(followBool);
                    if(followBool){
                    followBtn.value = "Un-Follow";
                    } else{
                    followBtn.value = "Follow";
                    }
                });
            });
        });
    };
    

    // Delete Item
    const deleteItemForm = document.querySelectorAll("form[name=deleteItem]");

    deleteItemForm.forEach(form => {
        form.addEventListener("submit", function(e){
            e.preventDefault();
            const listItemId = e.target.querySelector("input[name=listItemId]").value;
            const data = new FormData(e.target);
            const values = Object.fromEntries(data);

            const response = fetch(`/delete_list_item/${listItemId}`,{
                method : "POST",
                headers: {
                    "X-CSRFToken": values.csrfmiddlewaretoken
                },
            });
            form.parentElement.innerHTML = "Item has been deleted";
        });
    });

    // Completed items

    const checkboxComplete = document.querySelectorAll("input[name=checkboxComplete]");

    checkboxComplete.forEach(input =>{

        //Set checkbox depending on completed boolean
        const formItem = input.parentElement;
        const liItem = formItem.parentElement;
        const ulItem = liItem.parentElement;
        const listItemId = liItem.querySelector("input[name=completeListItemId]").value;

        const getResponse = fetch(`/check_complete/${listItemId}`,{
            method : "GET",
        }).then(response => response.json()).then(data =>{
            const completedBool = data.listItem.completed
            if (completedBool){
                input.checked = true;
                liItem.style.setProperty("text-decoration", "line-through");
                ulItem.insertAdjacentElement("beforeend", liItem);
            }else{
                input.checked = false;
            };
        });

        // Clicking checkbox
        input.addEventListener("change", function(e){
            e.preventDefault();
            const data = new FormData(formItem);
            const values = Object.fromEntries(data);

            const response = fetch(`/complete_list_item/${listItemId}`,{
                method : "PUT",
                headers: {
                    "X-CSRFToken": values.csrfmiddlewaretoken
                },
            }).then(response => response.json()).then(data =>{
                const completedBool = data.listItem.completed;
                if (completedBool){
                    input.checked = true;
                    liItem.style.textDecoration = "line-through";
                    ulItem.insertAdjacentElement("beforeend", liItem);
                }else if (completedBool == false){
                    input.checked = false
                    liItem.style.textDecoration = "none";
                };
            });
        });
    });
})
