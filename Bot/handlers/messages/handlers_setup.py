from handlers.messages import commands
from handlers.messages import data_collecting

from aiogram import Router

def message_handlers_setup(router: Router) -> None:
    commands.setup(router)
    data_collecting.setup(router)
    router.message.register(commands.clean_work_station)