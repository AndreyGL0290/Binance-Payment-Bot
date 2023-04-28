import { Link } from "react-router-dom"
import { useState } from "react"
import basket from "../basket"
import tg from '../telegram'
import '../css/basket.css'

const Basket = () => {
    window.scrollTo(0,0)
    window.sessionStorage.setItem('products', JSON.stringify(basket.products))
    if (!tg.BackButton.isVisible) tg.BackButton.show()
    if (!tg.MainButton.isVisible) tg.MainButton.show()

    let [x, setDelete] = useState(false)
    // document.getElementsByClassName('middle-container')[0].style.justifyContent = 'center'
    if (Object.keys(basket.products).length === 0){
        tg.MainButton.hide()
        return (
            <div className="after-label-container">
                <span>Ваша корзина пуста<br/>Посмтрите что-нибудь еще<br/><br/></span>
                <Link className="get-more-button" to={'../'}>Посмотреть</Link>
            </div>
        )
    }

    return (
        <div className='basket-container'>
            {Object.values(basket.products).map(props => {
                return (
                    <BasketCard key={props.title} product={props} state={{x: x, setDelete: setDelete}}/>
                )
            })}
        </div>
    )
}

const BasketCard = (props) => {
    let price = props.product.price * props.product.quantity
    if (!props.product.postfix) price = Math.ceil(price)

    return (
        <div className='product-container'>
            <div className='content-container'>
                <div className='images-container'>
                    <div className="system-image" id="cross-image"
                    onClick={() => {
                        basket.deleteProduct(props.product.title)
                        props.state.setDelete(!props.state.x)
                    }}></div>

                    <Link to={'../products#'+props.product.parent} style={{width: 30 + 'px', height: 30 + 'px'}} onClick={() => {window.scrollTo(0,0)}}>
                        <div className="system-image" id="eye-image"></div>
                    </Link>

                </div>
                <span className='product-label'>{props.product.title}</span>

            </div>
            <div className='add-content-container'>
                <span className='product-quantity'>{props.product.quantity} {(props.product.postfix || 'кг').replace('₾/', '')}</span>
                <span className='product-price'>{price.toFixed(2)} ₾</span>
            </div>
        </div>
    )
}

export default Basket