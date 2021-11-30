let input = document.querySelector('input[type="file"]')
let btn = document.querySelector('#btn')

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// const csrftoken = getCookie('csrftoken');
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
btn.addEventListener('click', function (evt) {
    evt.preventDefault()
    let data = new FormData()
    data.append('images', input.files[0])
    data.append('category', 'kids')
    data.append('name', 'what')
    data.append('price', '100')
    data.append('inventory', '1')
    data.append('intro', 'introduction')
    fetch('/api/items/', {
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        body: data
    }).then(res => {
            console.log(res.headers)
            console.log(res.body)
        }
    ).catch(e => {
            console.log(e)
        }
    )
})