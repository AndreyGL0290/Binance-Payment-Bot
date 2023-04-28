import basket from './basket'
import homePageReroute from './RerouteFunc'

let tg = window.Telegram.WebApp

tg.MainButton.color = '#FFBF00'
tg.MainButton.textColor = '#000000'

tg.MainButton.text = "Подтвердить заказ"

tg.MainButton.onClick(() => {
    window.sessionStorage.clear()
    
    let data = {}

    // Shortens basket product data so only valuable information is send
    for (let i = 0; i < Object.keys(basket.products).length; i += 1){
        data[Object.keys(basket.products)[i]] = {'price': (basket.products[Object.keys(basket.products)[i]].price), 'quantity': basket.products[Object.keys(basket.products)[i]].quantity, 'postfix': (basket.products[Object.keys(basket.products)[i]].postfix || '₾/кг')}
    }

    tg.sendData(JSON.stringify(data))
})

tg.BackButton.onClick(homePageReroute)

export default tg