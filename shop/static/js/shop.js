window.onload = init

function init() {
    let btnCart = document.querySelectorAll('.btn.cart')

    for (let i = 0; i < btnCart.length; i++) {
        btnCart[i].addEventListener('click', addCart)
    }
}
