from handlers.callbacks import basket_logic
from handlers.callbacks import data_collecting

from aiogram import Router

def callback_handlers_setup(router: Router) -> None:
    basket_logic.setup(router)
    data_collecting.setup(router)