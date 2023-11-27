const todoCheckIconList = document.getElementsByClassName('todoCheckIcon')
const todoRemoveIconnList = document.getElementsByClassName('todoRemoveIcon')


for (let index = 0; index < todoCheckIconList.length; index++) {
    todoCheckIconList[index].addEventListener("click", handleChangeStatus);
}

for (let index = 0; index < todoRemoveIconnList.length; index++) {
    todoRemoveIconnList[index].addEventListener("click", handleRemoveTodo);
}


function handleChangeStatus(e) {
    let todoIcon = e.target
    let todoID = todoIcon.getAttribute('todoID')
    if (todoID) {
        fetch(`/status/${todoID}`).then((res) => res.json()).then((data) => {
            if (data.status) {
                e.target.parentNode.classList.add('check')
                e.target.src = '/static/img/check.png'

            } else {
                e.target.parentNode.classList.remove('check')
                e.target.src = '/static/img/circle.png'
            }
        })
    }
}

function handleRemoveTodo(e) {
    let todoIcon = e.target
    let todoID = todoIcon.getAttribute('todoID')
    if (todoID) {
        fetch(`/delete/${todoID}`).then((res) => res.json()).then((data) => {
            if (data.delete) {
                e.target.parentNode.classList.add('hidden')
                const leftLi = e.target.parentNode.parentNode.querySelectorAll('li:not(.hidden)')
                if (leftLi.length === 0) {
                    // 刷新页面
                    location.reload()
                }
            }
        })
    }
}
