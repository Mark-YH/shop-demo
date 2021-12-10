let submitCreateItem = document.querySelector('#submit')
let showCreateItemForm = document.querySelector('#btnCreateItem')

const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


reset.addEventListener('click', function (evt) {
    let rs = document.querySelector('#submitResult')
    for (let i = 0; i < rs.childElementCount; i++) {
        rs.removeChild(rs.childNodes[i])
    }
})

showCreateItemForm.addEventListener('click', function (evt) {
    document.querySelector('#formCreateItem').removeAttribute('hidden')
})

submitCreateItem.addEventListener('click', function (evt) {
    evt.preventDefault()

    let rs = document.querySelector('#submitResult')
    let msg = ''
    fetch('/api/items/', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: getFormData()
    }).then(res => {
        if (res.ok) {
            return res.json()
        } else {
            throw res.json()
        }
    }).then(jsonData => {
        console.log(jsonData)

        let form = document.querySelectorAll('input, textarea')
        for (let i = 0; i < form.length; i++) {
            form[i].value = ''
        }
        let selectors = document.querySelectorAll('select')
        for (let i = 0; i < selectors.length; i++) {
            selectors[i].selectedIndex = 0
        }
        msg = '上傳成功'
    }).catch(e => {
        console.log(e)
        msg = '上傳失敗'
    }).finally(() => {
        for (let i = 0; i < rs.childElementCount; i++) {
            rs.childNodes[i].remove()
        }
        let element = document.createElement('p')
        element.innerHTML = msg
        rs.appendChild(element)
    })
})