from json import dumps
import math

class Basket():
    def __init__(self, products: dict = {}, order_params: dict = {}, delivery_tax: int = 0):
        self.products = products
        self.order_params = order_params
        self.delivery_tax = delivery_tax
    
    def add(self, name: str, product: dict) -> None:
        self.products[name] = product
    
    def beautified_output(self) -> str:
        order = ''
        for name, product in self.products.items():
            total_price = f"{float(product['price'])*float(product['quantity']):0.2f}"
            if product['postfix'] == '₾/кг':
                total_price = math.ceil(float(total_price))
            order += f"{name} {product['quantity']} * {product['price']} = {total_price} ₾\n"
        return order.strip('\n')
    
    def order_price(self):
        return sum([math.ceil(float(product['price'])*float(product['quantity'])) if product['postfix'] == '₾/кг' else float(f"{float(product['price'])*float(product['quantity']):0.2f}") for _, product in self.products.items()])
    
    def delivery_alert(self) -> str:
        if self.order_price() < 50:
            return "<b>\nСтоимость доставки: 5 ₾</b>"
        return "<b>\nСтоимость доставки: 0 ₾</b>"

    def delete(self, name: str) -> None:
        del self.products[name]

    def save(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.order_params[k] = v
  
    def get_params(self, param: str):
        return self.order_params.get(param)

    def toJSON(self) -> str:
        return dumps(self, default=lambda self: self.__dict__, sort_keys=True, indent=4)