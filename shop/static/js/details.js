window.onload = init

function init() {
    let btnAddCart = document.querySelector('.btn.cart')
    let btnBuy = document.querySelector('.btn.buy')
    let btns = document.querySelectorAll('.admin.close')
    for (let i = 0; i < btns.length; i++) {
        btns[i].remove()
    }
    btnAddCart.addEventListener('click', function (evt) {
        addCart(evt)
    })

    btnBuy.addEventListener('click', function (evt) {
        addCart(evt)
        window.location.replace('/cart/')
    })
}