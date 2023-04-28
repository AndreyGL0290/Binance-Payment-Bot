from dotenv import load_dotenv
from os import getenv
import sys
load_dotenv()

# Enables import from upper directories
sys.path.append(getenv('ROOT_PATH'))

# Configuration data for bot
from basic_logic.config import *

from keyboards.static import web_app_keyboard, basket_buttons, payment_type_buttons, change_buttons, change_notes_buttons, phone_number_keyboard, skip_button, web_app_keyboard
from DB_logic.send_information import commit_order_to_DB
from DB_logic.get_info import UserData
from handlers.common_functions import get_data_from_state
from data.load_data import load_text_template
from basic_logic.product_logic import Basket

from aiogram.fsm.context import FSMContext
from aiogram.methods.send_message import SendMessage
from aiogram.methods.send_contact import SendContact
from aiogram import Router, types, F

### Data collection handlers ###
# Asks for prefered payment type
@get_data_from_state
async def self_delivery(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()

    # Saving information about order
    basket.save(delivery='самовывоз', address=None)
    basket.delivery_tax = 0
    
    await callback_query.message.edit_text('Выберите способ оплаты', reply_markup=payment_type_buttons())

    await state.set_state(Form.get_contact) if not UserData.user_exist(callback_query.from_user.id) else await state.set_state(Form.skip_contact)

    return basket

# Asks user to enter address for delivery and updates products in order
@get_data_from_state
async def ask_for_address(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    # Specifies delivery_tax
    basket.delivery_tax = 5 if basket.order_price() < 50 else 0

    await callback_query.answer()
    await callback_query.message.edit_text('Введите адресс для доставки')

    current_state = await state.get_state()

    await state.set_state(Form.delivery_time) if current_state != Form.confirmation.state else await state.set_state(Form.change_address)

    return basket

# Saves user address and asks prefered payment type
@get_data_from_state
async def ask_for_payment_type(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    basket.save(delivery_time=callback_query.data)

    await callback_query.answer()
    await callback_query.message.edit_text('Выберите способ оплаты', reply_markup=payment_type_buttons())

    await state.set_state(Form.pay_state) if not UserData.user_exist(callback_query.from_user.id) else await state.set_state(Form.skip_contact)

    return basket

@get_data_from_state
async def ask_for_change(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket): # If answer is cash
    await callback_query.answer()
    basket.save(payment='наличные')
    await callback_query.message.edit_text('Нужна ли вам сдача?', reply_markup=change_buttons())
    await state.set_state(Form.ask_note_to_have_change_for) if not UserData.user_exist(callback_query.from_user.id) else await state.set_state(Form.skip_contact)
    
    return basket

async def change_is_required(callback_query: types.CallbackQuery, state: FSMContext): # If answer is yes
    await callback_query.answer()
    await callback_query.message.edit_text('С какой купюры вам нужна сдача?', reply_markup=change_notes_buttons())
    await state.set_state(Form.get_contact) if not UserData.user_exist(callback_query.from_user.id) else await state.set_state(Form.skip_contact)


# Saves prefered payment type and asks for contact
@get_data_from_state
async def ask_for_contact(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()
    
    if callback_query.data == 'card':
        basket.save(payment='перевод на карту')
    elif callback_query.data != 'no':
        basket.save(note=callback_query.data)

    await callback_query.message.delete()
    
    message = await SendMessage(chat_id=callback_query.from_user.id, text='Нажмите на кнопку "Поделиться контактом", чтобы менеджеру было легче с вами связаться', reply_markup=phone_number_keyboard())
    message_id = message.message_id
    await state.update_data({'basket': basket.toJSON(), 'message_to_delete': message_id})

    await state.set_state(Form.phone_number)

    return basket

# Saves user contact and asks for phone number
@get_data_from_state
async def change_number(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await SendMessage(chat_id=callback_query.from_user.id, text="Введите местный номер телефона")
    await state.set_state(Form.change_number)
    return basket

@get_data_from_state
async def ask_for_phone_number(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()
    
    if callback_query.data == 'card':
        basket.save(payment='перевод на карту')
    elif callback_query.data != 'no':
        basket.save(note=callback_query.data)
    
    await callback_query.message.edit_text(text="Введите местный номер телефона, если такой есть", reply_markup=skip_button())
    await state.set_state(Form.name)
    return basket

@get_data_from_state
async def ask_for_name(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()

    basket.save(phone_number=None)

    await callback_query.message.delete()
    await SendMessage(chat_id=callback_query.from_user.id, text='Как к вам можно обращаться?', reply_markup=web_app_keyboard())

    await state.set_state(Form.commit_order)
    return basket

# Sends info about order into DB and to operators
@get_data_from_state
async def confirm_order(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()

    # Saving order to db and sending it to project customer
    basket.save(username=f'@{callback_query.from_user.username}')
    order_id = "Данные не были занесены в БД"

    try:
        order_id = commit_order_to_DB(callback_query.from_user.id, basket)
    except Exception as db_error:
        print(f'{db_error=}')
    
    telegram_phone_number = f"{basket.get_params('telegram_phone_number')}" if basket.get_params('telegram_phone_number') else f'{UserData.DB_get_tg_phone(callback_query.from_user.id)}'
    phone_number = f"<b>Телефон</b>: {basket.get_params('phone_number')}" if basket.get_params('phone_number') else ''
    address = f"<b>Доставка по адресу</b>: {basket.get_params('address')}" if basket.get_params('delivery') == 'доставка' else '<b>Самовывоз</b>'
    delivery_time = f"\n<b>Предпочитаемое время доставки</b>: " + basket.get_params('delivery_time') if basket.get_params('delivery_time') else ''
    payment = f"{basket.get_params('payment')}"
    
    if basket.get_params('payment') == 'наличные':
        payment = f"{basket.get_params('payment')}, сдача с купюры в {basket.get_params('note')} ₾" if basket.get_params('note') else f"{basket.get_params('payment')}, сдача не нужна"

    for id in getenv('MANAGER_IDS').split(', '):
        try:
            message = await SendMessage(chat_id=int(id), text=load_text_template('data/text_snippets/order_info_manager.txt').format(order_id=order_id,
                                                                                                         name=basket.get_params('name'),
                                                                                                         order_content=basket.beautified_output(),
                                                                                                         delivery_tax=f'<b>Стоимость доставки</b>: {basket.delivery_tax}',
                                                                                                         telegram_phone_number=telegram_phone_number,
                                                                                                         phone_number=phone_number,
                                                                                                         delivery_time=delivery_time,
                                                                                                         total_price=f'{basket.order_price() + basket.delivery_tax:0.2f}',
                                                                                                         address=address,
                                                                                                         payment_type=payment))
            await SendContact(chat_id=int(id), phone_number=telegram_phone_number, first_name=basket.get_params('firstname'), reply_to_message_id=message.message_id)
        except Exception as error:
            await SendMessage(chat_id=getenv('PROGRAMMER_ID'), text=f"An error occured:\n{error}\n\nOrder ID: {order_id}\nEmployer Telegram ID: {id}")
    if basket.get_params('delivery') == 'доставка':
        for id in getenv('DELIVERYMAN_IDS').split(', '):
            try:
                message = await SendMessage(chat_id=int(id), text=load_text_template('data/text_snippets/order_info_deliveryman.txt').format(order_id=order_id,
                                                                                                            name=basket.get_params('name'),
                                                                                                            total_price=f'{basket.order_price() + basket.delivery_tax:0.2f}',
                                                                                                            payment_type=payment,
                                                                                                            address=address,
                                                                                                            delivery_time=delivery_time,
                                                                                                            phone_number=phone_number))
                await SendContact(chat_id=int(id), phone_number=telegram_phone_number, first_name=callback_query.from_user.first_name, reply_to_message_id=message.message_id)
            except Exception as error:
                await SendMessage(chat_id=getenv('PROGRAMMER_ID'), text=f"An error occured:\n{error}\n\nOrder ID: {order_id}\nEmployer Telegram ID: {id}")

    await SendMessage(chat_id=callback_query.from_user.id, text='Спасибо, Ваш заказ принят!\nМенеджер свяжется с вами в ближайшее время.', reply_markup=web_app_keyboard())
    
    basket = Basket()

    await state.set_state(Form.web_app)
    
    return basket

# If user canceled his order
@get_data_from_state
async def cancel_order(callback_query: types.CallbackQuery, state: FSMContext, basket: Basket):
    await callback_query.answer()
    await callback_query.message.edit_text(load_text_template('data/text_snippets/basket.txt').format(content=basket.beautified_output(),
                                                                                                      summary=f'{basket.order_price():0.2f}',
                                                                                                      delivery_type_alert=basket.delivery_alert()),
                                                                                                      reply_markup=basket_buttons())

    await state.set_state(Form.delivery_conditions)
    
    return basket

def setup(router: Router):
    router.callback_query.register(self_delivery, F.data=='self-delivery', Form.delivery_conditions)

    router.callback_query.register(ask_for_address, F.data=='delivery', Form.delivery_conditions)
    router.callback_query.register(ask_for_address, F.data=='change address', Form.confirmation)

    router.callback_query.register(ask_for_payment_type, Form.payment_conditions)

    router.callback_query.register(ask_for_change, F.data=='cash')
    
    router.callback_query.register(change_is_required, F.data=='yes', Form.ask_note_to_have_change_for)
    router.callback_query.register(change_is_required, F.data=='yes', Form.skip_contact)
    router.callback_query.register(confirm_order, F.data=='confirm', Form.confirmation)
    router.callback_query.register(cancel_order, F.data=='deny', Form.confirmation)
    router.callback_query.register(change_number, F.data=='change number', Form.confirmation)

    router.callback_query.register(ask_for_phone_number, Form.skip_contact)

    router.callback_query.register(ask_for_contact, Form.get_contact)
    router.callback_query.register(ask_for_contact, F.data=='card')
    router.callback_query.register(ask_for_contact, Form.ask_note_to_have_change_for)


    router.callback_query.register(ask_for_name, Form.name)
