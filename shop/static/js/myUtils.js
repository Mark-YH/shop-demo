function getCookie(cookieName) {
    let cookieList = document.cookie.split(';')
    for (let i = 0; i < cookieList.length; i++) {
        if (cookieList[i].includes(cookieName)) {
            return cookieList[i].split(cookieName + '=')[1]
        }
    }
    return null
}

function getExpires() {
    let date = new Date()
    date.setTime(date.getTime() + 3600 * 1000)
    return date.toUTCString()
}

function addCart(evt) {
    let itemId = evt.currentTarget.getAttribute('id').split('-')[1]
    let cartCookie = getCookie('cart')
    let obj = Object()

    if (cartCookie != null) {
        obj = JSON.parse(cartCookie)
    }

    if (obj[itemId]) {
        obj[itemId] += 1
    } else {
        obj[itemId] = 1
    }
    document.cookie = 'cart=' + JSON.stringify(obj) + ';path=/;expires=' + getExpires()
}