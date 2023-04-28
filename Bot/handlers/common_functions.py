from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

# Configuration data for bot
from basic_logic.config import *
from json import loads
from aiogram.fsm.context import FSMContext
from basic_logic.product_logic import Basket

def get_data_from_state(func):
    '''Gets data from the current state, passes it to the main function, pushes it back to the state'''

    async def inner(action, state: FSMContext):
        # Before main function execution
        data = await state.get_data()
        data = loads(data['basket'])

        basket = Basket(products=data['products'], order_params=data['order_params'], delivery_tax=data['delivery_tax'])

        basket: Basket = await func(action, state, basket) # Main function execution
        
        # After main function execution
        await state.update_data(basket=basket.toJSON())
    
    return inner
