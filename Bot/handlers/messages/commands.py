from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

# Configuration data for bot
from basic_logic.config import *

# Importing self-made modules
from keyboards.static import web_app_keyboard
from data.load_data import load_text_template
from basic_logic.product_logic import Basket

from aiogram.filters.command import Command
from aiogram.methods.send_message import SendMessage
from aiogram.methods.delete_message import DeleteMessage
from aiogram.fsm.context import FSMContext
from aiogram import types, Router

# Sends greeting message
async def greetings(message: types.Message, state: FSMContext):
    await message.reply('Greetings in {your_shop_name}', reply_markup=web_app_keyboard())
    await state.set_state(Form.web_app)

    # Making instances for current user, which will be used further
    basket = Basket()
    
    await state.set_data({})
    await state.update_data(basket=basket.toJSON())

# Sends contacts
async def contacts(message: types.Message):
    await DeleteMessage(chat_id=message.from_user.id, message_id=message.message_id)
    await SendMessage(chat_id=message.from_user.id, text=load_text_template('data/text_snippets/contacts.txt'), disable_web_page_preview=True)

# Deletes messages that were not supposed to be sent
async def clean_work_station(message: types.Message):
    await DeleteMessage(chat_id=message.from_user.id, message_id=message.message_id)

def setup(router: Router):
    router.message.register(greetings, Command('start'))
    router.message.register(contacts, Command('contacts'))