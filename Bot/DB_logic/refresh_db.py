from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

from basic_logic.config import conn, cur

def create_tables():
    cur.execute("CREATE TABLE customers(id integer primary key autoincrement, tg_id varchar(40), username varchar(50), name varchar(255), telegram_phone_number varchar(20), phone_number varchar(20));")
    cur.execute("CREATE TABLE orders(customer_id integer, content varchar(65535), price int NOT NULL, delivery_type varchar(20), address varchar(65535), delivery_tax int, delivery_time varchar(30), payment_type varchar(20));")


def drop_tables():
    cur.execute("DROP TABLE customers")
    cur.execute("DROP TABLE orders")

    conn.commit()

try:
    drop_tables()
    create_tables()
except:
    create_tables()
    