from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

# Configuration data for bot
from basic_logic.config import *

from handlers.common_functions import get_data_from_state
from basic_logic.product_logic import Basket

from aiogram.fsm.context import FSMContext
from aiogram import types, Router, F

# Deletes basket content
@get_data_from_state
async def clear_basket(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()

    basket = Basket()
    await state.update_data(basket=basket.toJSON())

    await callback_query.message.edit_text('❌ Ваша корзина пуста')

    await state.set_state(Form.web_app)
    
    return basket


def setup(router: Router):
    router.callback_query.register(clear_basket, F.data=='clear', Form.delivery_conditions)