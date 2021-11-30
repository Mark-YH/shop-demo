let elementEdit = document.querySelectorAll('.admin-btn-edit')
let adminButtonDelete = document.querySelectorAll('.admin-btn-delete')
let modalEdit = document.querySelector('#modalEdit')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

modalEdit.querySelector('#createItemFormTitle').remove()
modalEdit.querySelector('#reset').remove()
modalEdit.querySelector('#submit').remove()
modalEdit.querySelector('#formCreateItem').removeAttribute('hidden')

function editItem(evt) {
    console.log(evt.currentTarget)
}


function delItem(evt) {
    let item_id = evt.currentTarget.getAttribute('id').split('-')[1]

    let confirm = document.querySelector("#confirmDel")
    confirm.addEventListener('click', function (innerEvt) {
        fetch('/api/items/' + item_id + '/', {
                method: 'DELETE',
                header: {'X-CSRFToken': csrftoken},
            }
        ).then(res => {
            if (res.ok)
                console.log('---deleted---')
            console.log('Response' + res)
        }).catch(e => {
            console.log(e)
        }).finally(() => {
            confirm.removeEventListener('click', this)
            location.reload()
        })
    })
}

for (let i = 0; i < adminButtonDelete.length; i++) {
    adminButtonDelete[i].addEventListener('click', delItem)
}

for (let i = 0; i < adminButtonDelete.length; i++) {
    elementEdit[i].addEventListener('click', editItem)
}