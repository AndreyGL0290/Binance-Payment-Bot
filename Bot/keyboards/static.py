from aiogram.types import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM
from aiogram.types import ReplyKeyboardMarkup as RKM, KeyboardButton as KB, WebAppInfo

from data.load_data import load_json

# Creates inline buttons normaly below the basket content message
def basket_buttons():

    clear = IKB(text='Очистить', callback_data='clear')
    self_delivery = IKB(text='Самовывоз', callback_data='self-delivery')
    delivery = IKB(text='Доставка', callback_data='delivery')

    inline_kb = IKM(inline_keyboard=[
        [clear],
        [self_delivery, delivery]
    ])

    return inline_kb

def delivery_time_buttons():
    times = load_json('data/times.json')['times']
    
    inline_kb = IKM(inline_keyboard=[[IKB(text=i, callback_data=i)] for i in times])

    return inline_kb

def payment_type_buttons():

    cash = IKB(text='Наличные', callback_data='cash')
    card = IKB(text='Карта', callback_data='card')


    inline_kb = IKM(inline_keyboard=[
        [cash],
        [card]
    ])

    return inline_kb

def change_buttons():
    yes = IKB(text='Да', callback_data='yes')
    no = IKB(text='Нет', callback_data='no')

    inline_kb = IKM(inline_keyboard=[
        [yes, no]
    ])

    return inline_kb

def change_notes_buttons():

    note_5 = IKB(text='5 ₾', callback_data='5')
    note_10 = IKB(text='10 ₾', callback_data='10')
    note_20 = IKB(text='20 ₾', callback_data='20')
    note_50 = IKB(text='50 ₾', callback_data='50')
    note_100 = IKB(text='100 ₾', callback_data='100')

    inline_kb = IKM(inline_keyboard=[
        [note_5, note_10, note_20],
        [note_50, note_100]
    ])

    return inline_kb

def skip_button():
    skip = IKB(text='Пропустить', callback_data='skip')
    inline_kb = IKM(inline_keyboard=[
        [skip]
    ])

    return inline_kb

def confirm_buttons(change_delivery_button: bool = False):
    confirm = IKB(text='Подтвердить', callback_data='confirm')
    deny = IKB(text='Отменить', callback_data='deny')
    change_address = IKB(text='Изменить адрес доставки', callback_data='change address')
    change_phone_number = IKB(text='Изменить номер телефона', callback_data='change number')

    inline_kb = IKM(inline_keyboard=[
        [deny, confirm],
        [change_phone_number]
    ])
    if change_delivery_button:
        inline_kb = IKM(inline_keyboard=[
            [deny, confirm],
            [change_address],
            [change_phone_number]
        ])

    return inline_kb

# Creates reply keyboard buttons above actual user keyboard
def web_app_keyboard():
    web_app = WebAppInfo(url="https://andreygl0290.github.io/Binance-Payment-Bot/#/")
    keyboard = RKM(
        keyboard=[
            [KB(text="Сделать заказ", web_app=web_app)]
        ], resize_keyboard=True)
    
    return keyboard

def phone_number_keyboard():
    keyboard = RKM(
        keyboard=[
            [KB(text="Поделиться контактом", request_contact=True)]
        ], resize_keyboard=True, one_time_keyboard=True
    )

    return keyboard