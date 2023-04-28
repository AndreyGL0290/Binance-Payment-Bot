from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

from basic_logic.product_logic import Basket
from DB_logic.get_info import UserData
from basic_logic.config import conn, cur

def commit_order_to_DB(user_id: int, basket: Basket):
    content = ''
    for product, value in basket.products.items():
        content = content + product + ' ' + str(value['quantity']) + value['postfix'].replace('₾/', '') + ', '
    content = content.strip(', ')

    if not UserData.user_exist(user_id):
        cur.execute(f"INSERT INTO customers (tg_id, username, name, telegram_phone_number, phone_number) VALUES ({user_id}, '{basket.get_params('username')}', '{basket.get_params('name')}', '{basket.get_params('telegram_phone_number')}', '{basket.get_params('phone_number')}')")
    customer_id = cur.execute(f"SELECT id FROM customers WHERE tg_id={user_id}").fetchall()[0][0]
    
    cur.execute(f"INSERT INTO orders (customer_id, content, price, delivery_type, address, delivery_tax, delivery_time, payment_type) VALUES ({customer_id}, \"{content}\", {basket.order_price() + basket.delivery_tax}, '{basket.get_params('delivery')}', '{basket.get_params('address')}', {basket.delivery_tax}, '{basket.get_params('delivery_time')}', '{basket.get_params('payment')}')")
    order_id = cur.execute("SELECT last_insert_rowid() FROM customers").fetchall()[0][0]

    conn.commit()
    return order_id