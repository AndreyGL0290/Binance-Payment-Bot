import { Link, useLocation } from "react-router-dom"
import { useEffect, useState } from "react"
import '../css/placeholder.css'
import basket from "../basket"
import tg from '../telegram'
import '../css/products.css'
import Image from "./Image"
import menu from '../menu'

const Products = () => {
    if (tg.MainButton.isVisible) tg.MainButton.hide()
    if (!tg.BackButton.isVisible) tg.BackButton.show()

    const location = useLocation()
    let [products, setProducts] = useState([])
    let [button, setButton] = useState(<></>)
    
    useEffect(() => {
        setButton(
        <div className="basket-button-container">
            <Link to="../basket" className="basket-button" onClick={() => {window.scrollTo(0,0)}}>Перейти в корзину</Link>
        </div>
        )
        if (Object.keys(basket.products).length === 0) setButton(<></>)
    }, [products])

    let data = []
    
    let category = location.hash.replace('#', '')
    let products_list = {}
    console.log(menu)
    for (let i=0; i<Object.keys(menu[category]).length; i++){
        console.log(typeof menu[category][Object.keys(menu[category])[i]], menu[category][Object.keys(menu[category])[i]])
        if (typeof menu[category][Object.keys(menu[category])[i]] === 'object') products_list[Object.keys(menu[category])[i]] = menu[category][Object.keys(menu[category])[i]]
    }
    console.log(products_list)
    for (let i = 0; i < Math.ceil(Object.keys(products_list).length / 2); i++){
        let sub_data = []
        for (let j = i*2; j < 2*(i + 1); j++){
            if (!Object.keys(products_list)[j]) continue
            if (basket.getProduct(menu[category][Object.keys(products_list)[j]].title)) {
                menu[category][Object.keys(products_list)[j]].state = {products: products, setProducts: setProducts}
                sub_data.push(menu[category][Object.keys(products_list)[j]])
                continue
            }
            menu[category][Object.keys(products_list)[j]].parent = category
            menu[category][Object.keys(products_list)[j]].state = {products: products, setProducts: setProducts}
            sub_data.push(menu[category][Object.keys(products_list)[j]])
        }
        if (sub_data.length !== 0) data.push(sub_data)
    }
    return (
    <>
        <div className="inner-container">
            {data.map(props => {
                return (
                    <ProductCard key={props[0].title} product={props}/>
                )
            })}
        </div>
        {button}
    </>
    )
}

const ProductCard = (props) => {
    props = props.product
    if (props.length === 2) return (
        <div className="cards">
            <div className="label-container">
                <span className="card-label">{props[0].title}</span>
                <span className="card-label">{props[1].title}</span>
            </div>
            <div className="image-container">
                <Image src={process.env.PUBLIC_URL + props[0].imagePath} sub_title={props[0].sub_title}/>
                <Image src={process.env.PUBLIC_URL + props[1].imagePath} sub_title={props[1].sub_title}/>
            </div>
            <div className="price-container">
                <span className="card-price">{props[0].price + ' ' + (props[0].postfix || '₾/кг')}</span>
                <span className="card-price">{props[1].price + ' ' + (props[1].postfix || '₾/кг')}</span>
            </div>
            <div className="button-container">
                <CardFooter product={props[0]} state={props[0].state} />
                <CardFooter product={props[1]} state={props[1].state} />
            </div>
        </div>
    )
    else return (
        <div className="cards">
            <div className="label-container">
                <span className="card-label">{props[0].title}</span>
            </div>
            <div className="image-container">
                <Image src={process.env.PUBLIC_URL + props[0].imagePath} sub_title={props[0].sub_title}/>
            </div>
            <div className="price-container">
                <span className="card-price">{props[0].price + ' ' + (props[0].postfix || '₾/кг')}</span>
            </div>
            <div className="button-container">
                <CardFooter product={props[0]} state={props[0].state} />
            </div>
        </div>
    )
}

const CardFooter = (props) => {
    let startValue
    if (basket.products[props.product.title]) startValue = basket.products[props.product.title].quantity
    else startValue = 0
    const [quantity, setQuantity] = useState(startValue)

    let x = props.product.measure || 0.5

    if (quantity === 0){
        return (
            <button className="card-button" onClick={() => {
                setQuantity(quantity + x)
                
                basket.addProduct(props.product.title, {title: props.product.title, parent: props.product.parent, price: props.product.price, postfix: props.product.postfix}, x)
                window.sessionStorage.setItem('products', JSON.stringify(basket.products))

                if (Object.keys(basket.products).length <= 1) props.state.setProducts(Object.keys(basket.products))                
            }}>Добавить</button>
        )
    }
    else {
        let quantityPostfix = props.product.postfix || 'кг'
        return (
            <div className="product-menu-container">
                <div className="system-image" id="minus-image"
                onClick={() => {
                    setQuantity(quantity - x)
                    basket.setQuantity(props.product.title, -x)
                    window.sessionStorage.setItem('products', JSON.stringify(basket.products))
                    
                    if (Object.keys(basket.products).length === 0) props.state.setProducts([])
                }}></div>

                <span className="quantity-label" onDoubleClick={e => {e.preventDefault()}}>{quantity} {quantityPostfix.replace('₾/', '')}</span>

                <div className="system-image" id="plus-image"
                onClick={() => {
                    setQuantity(quantity + x)
                    basket.setQuantity(props.product.title, x)
                    window.sessionStorage.setItem('products', JSON.stringify(basket.products))
                }}></div>
            </div>
        )
    }
}

export default Products