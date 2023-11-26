const todoClassList = document.getElementsByClassName('todo')


for (let index = 0; index < todoClassList.length; index++) {
    todoClassList[index].addEventListener("click", handleChangeStatus);
}


function handleChangeStatus(e) {
    console.log(111, e.target.getAttribute('todoID'))
}

