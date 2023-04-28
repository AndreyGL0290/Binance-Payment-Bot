from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

from basic_logic.config import conn, cur

def select_items():
    res1 = cur.execute('SELECT * FROM customers')
    result1 = res1.fetchall()
    print(result1)

    res2 = cur.execute('SELECT * FROM orders')
    result2 = res2.fetchall()
    print(result2)
    
    conn.commit()

select_items()
