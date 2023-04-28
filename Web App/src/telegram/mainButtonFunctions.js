import basket from '../basket'

export const sendDataToBot = (tg) => {
    window.sessionStorage.clear()
    
    let data = {}

    // Shortens basket product data so only valuable information is send
    for (let i = 0; i < Object.keys(basket.products).length; i += 1){
        data[Object.keys(basket.products)[i]] = {'price': (basket.products[Object.keys(basket.products)[i]].price), 'quantity': basket.products[Object.keys(basket.products)[i]].quantity, 'postfix': (basket.products[Object.keys(basket.products)[i]].postfix || '₾/кг')}
    }

    tg.sendData(JSON.stringify(data))
}

export const redirectPage = (hash) => {
    window.location.hash = hash
}

export const mainButtonBasket = (tg) => {
    tg.MainButton.text = 'Перейти в корзину'
}

export const mainButtonConfirm = (tg) => {
    tg.MainButton.text = "Подтвердить заказ"
}