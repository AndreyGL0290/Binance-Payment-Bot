// Here all products that user chooses are stored
class Basket{
    constructor(){
        this.products = {}
    }

    setQuantity(title, quantity){
        this.products[title].quantity += quantity
        if (this.products[title].quantity === 0) this.deleteProduct(title)
    }

    addProduct(title, product, quantity){
        this.products[title] = product
        this.products[title].quantity = quantity
    }

    getProduct(title){
        return this.products[title]
    }

    deleteProduct(title){
        delete this.products[title]
    }
}

const basket = new Basket()

if (sessionStorage.getItem('products') !== null) basket.products = JSON.parse(sessionStorage.getItem('products'))

export default basket