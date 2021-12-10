function getFormData() {
    console.log('---get form data---')
    let data = new FormData()
    let input = document.querySelector('input[type="file"]')
    let category = document.querySelector('#categorySelect').value
    let itemName = document.querySelector('#itemName').value
    let intro = document.querySelector('#intro').value
    let price = document.querySelector('#price').value
    let inventory = document.querySelector('#inventory').value

    data.append('category', category)
    data.append('name', itemName)
    data.append('price', price)
    data.append('inventory', inventory)
    data.append('intro', intro)

    for (let i = 0; i < input.files.length; i++) {
        data.append('images', input.files[i])
    }
    console.log('--data--')
    console.log(data)
    console.log('--data--')
    return data
}