from dotenv import load_dotenv
from os import getenv
from json import loads
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

# Configuration data for bot
from basic_logic.config import *

from keyboards.static import delivery_time_buttons, confirm_buttons, basket_buttons, skip_button
from handlers.common_functions import get_data_from_state
from data.load_data import load_text_template
from DB_logic.get_info import UserData
from basic_logic.product_logic import Basket

from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram.methods.delete_message import DeleteMessage
from aiogram import types, Router, F


### Data collection handlers ###

# Gets the order form web application 
@get_data_from_state
async def get_order(message: types.Message, state: FSMContext, basket: Basket):
    for name, data in loads(message.web_app_data.data).items():
        basket.add(name, data)

    basket.save(firstname=message.from_user.first_name)
    delivery_tax = 5 if basket.order_price() < 50 else 0
    await SendMessage(chat_id=message.from_user.id, text=load_text_template('data/text_snippets/basket.txt').format(content=basket.beautified_output(),
                                                                                                                    summary=f'{basket.order_price() + delivery_tax:0.2f}',
                                                                                                                    delivery_type_alert=basket.delivery_alert()),
                                                                                                                    reply_markup=basket_buttons())

    await state.set_state(Form.delivery_conditions)

    return basket

# Saves user address for delivery and sends inline buttons for delivery time chose
@get_data_from_state
async def get_delivery_time(message: types.Message, state: FSMContext, basket: Basket):
    basket.save(delivery='доставка', address=message.text)
    
    await SendMessage(chat_id=message.from_user.id, text='Выберите время, в которое вам удобнее принять доставку', reply_markup=delivery_time_buttons())

    await state.set_state(Form.payment_conditions)

    return basket

# Saves user contact and asks for phone number
@get_data_from_state
async def ask_for_phone_number(message: types.Message, state: FSMContext, basket: Basket):
    basket.save(telegram_phone_number=message.contact.phone_number)
    
    await message.delete() # Deleting user message

    data = await state.get_data()
    await DeleteMessage(chat_id=message.from_user.id, message_id=data['message_to_delete']) # Deleting previous bot message
    await SendMessage(chat_id=message.from_user.id, text="Введите местный номер телефона, если такой есть", reply_markup=skip_button())
    
    await state.set_data({'basket': basket.toJSON()})
    await state.set_state(Form.name)
    return basket

@get_data_from_state
async def get_name(message: types.Message, state: FSMContext, basket: Basket):
    basket.save(phone_number=message.text)
    await SendMessage(chat_id=message.from_user.id, text='Как к вам можно обращаться?')

    await state.set_state(Form.commit_order)

    return basket

# Sends user a message with entered data, asks for confirmation of this data
@get_data_from_state
async def commit_order(message: types.Message, state: FSMContext, basket: Basket):
    load_dotenv(override=True)
    current_state = await state.get_state()
    if current_state == Form.commit_order.state:
        basket.save(name=message.text)
    elif current_state == Form.change_number.state:
        basket.save(phone_number=message.text)
    elif current_state == Form.change_address.state:
        basket.save(address=message.text)

    # Summing up given information
    total_cost = basket.order_price()
    delivery_tax = ''
    address = f"\n\n<b>Самовывоз по адресу</b>: {getenv('ADDRESS')}"
    delivery_time = ''

    if basket.get_params('delivery') == 'доставка':
        total_cost = total_cost + basket.delivery_tax
        delivery_tax = f'\n\n<b>Стоимость доставки</b>: {basket.delivery_tax} ₾'
        address = f"\n\n<b>Доставка по адресу</b>: {basket.get_params('address')}"
        delivery_time = f"\n\n<b>Удобное время для доставки</b>: {basket.get_params('delivery_time')}"
    
    telegram_phone_number = f"{basket.get_params('telegram_phone_number')}" if basket.get_params('telegram_phone_number') else f'{UserData.DB_get_tg_phone(message.from_user.id)}'
    phone_number = f'\n<b>Номер телефона для связи</b>: {basket.get_params("phone_number")}' if basket.get_params("phone_number") else ''

    payment = f"{basket.get_params('payment')}\n{getenv('CARD_DETAILS')}"
    if basket.get_params('payment') == 'наличные':
        payment = f"{basket.get_params('payment')}, сдача с купюры в {basket.get_params('note')} ₾" if basket.get_params('note') else f"{basket.get_params('payment')}, сдача не нужна"
    
    change_delivery_button = True if basket.get_params('delivery') == 'доставка' else False
    await SendMessage(chat_id=message.from_user.id, text=load_text_template('data/text_snippets/result.txt').format(products=basket.beautified_output(),
                                                                                                            delivery_tax = delivery_tax,
                                                                                                            address=address,
                                                                                                            total_cost=f'{total_cost:0.2f}',
                                                                                                            telegram_phone_number=telegram_phone_number,
                                                                                                            phone_number=phone_number,
                                                                                                            delivery_time=delivery_time,
                                                                                                            payment_type=payment),
                                                                                                            reply_markup=confirm_buttons(change_delivery_button))

    await state.set_state(Form.confirmation)

    return basket

def setup(router: Router):
    # Data collection
    router.message.register(get_order, F.web_app_data, Form.web_app)

    router.message.register(get_delivery_time, Form.delivery_time)

    router.message.register(ask_for_phone_number, F.contact, Form.phone_number)

    router.message.register(get_name, Form.name)

    router.message.register(commit_order, Form.commit_order)
    router.message.register(commit_order, Form.change_number)
    router.message.register(commit_order, Form.change_address)