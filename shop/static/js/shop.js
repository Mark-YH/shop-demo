let adminEditItem = document.querySelectorAll('.admin.btn.edit')
let adminButtonDelete = document.querySelectorAll('.admin.btn.delete')
let adminDeleteImage = document.querySelectorAll('.admin.close')
let modalEdit = document.querySelector('#modalEdit')

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

modalEdit.querySelector('#createItemFormTitle').remove()
modalEdit.querySelector('#reset').remove()
modalEdit.querySelector('#submit').remove()
modalEdit.querySelector('#formCreateItem').removeAttribute('hidden')

function setEditForm(evt) {
    let item_id = evt.currentTarget.getAttribute('id').split('-')[1]
    console.log(item_id)
    fetch('/api/items/' + item_id + '/', {
        method: 'GET'
    }).then(res => {
        if (res.ok) {
            return res.json()
        }
    }).then(jsonData => {
        for (const key in jsonData) {
            console.log(key + ': ' + jsonData[key])

            for (let i = 1; i < modalEdit.querySelector('#categorySelect').length; i++) {
                if (modalEdit.querySelector('#categorySelect').options[i].value.toLowerCase() === jsonData['category']) {
                    modalEdit.querySelector('#categorySelect').selectedIndex = i
                }
            }
            modalEdit.querySelector('#itemName').value = jsonData['name']
            modalEdit.querySelector('#intro').value = jsonData['intro']
            modalEdit.querySelector('#price').value = jsonData['price']
            modalEdit.querySelector('#inventory').value = jsonData['inventory']
            if (key === 'images') {
                for (const image in jsonData[key]) {
                    console.log('image: ' + JSON.stringify(jsonData[key][image]))
                }
            }
        }
    }).catch(e => {
        console.log(e)
    }).finally(() => {
        let confirm = document.querySelector('#confirmEdit')
        confirm.addEventListener('click', function (innerEvt) {
            fetch('/api/items/' + item_id + '/', {
                method: 'PUT',
                headers: {'X-CSRFToken': csrftoken},
                body: get_form_data(),
            }).then(res => {
                console.log(res)
            }).catch(e => {
                console.log(res)
            }).finally(() => {
                confirm.removeEventListener('click', this)
                location.reload()
            })
        })
    })
}


function delItem(evt) {
    let item_id = evt.currentTarget.getAttribute('id').split('-')[1]

    let confirm = document.querySelector("#confirmDelItem")
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

function deleteImage(evt) {
    let image = evt.currentTarget.getAttribute('id')
    index = image.search('-') + 1
    image = image.slice(index, image.length).replaceAll('/', '-*slash*-')
    console.log(image)
    let confirm = document.querySelector("#confirmDelImage")
    confirm.addEventListener('click', function (innerEvt) {
        fetch('/api/image/' + image + '/', {
            method: 'DELETE',
            headers: {'X-CSRFToken': csrftoken},
        }).then(res => {
            console.log(res.json())
            if (res.ok) {
                console.log('---image deleted---')
            }
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
    adminEditItem[i].addEventListener('click', setEditForm)
}

for (let i = 0; i < adminDeleteImage.length; i++) {
    adminDeleteImage[i].addEventListener('click', deleteImage)
}