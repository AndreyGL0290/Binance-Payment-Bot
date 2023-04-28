import logging
import asyncio

from dotenv import load_dotenv
from os import getenv

# Configuration data for bot
from basic_logic.config import router
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis 

# Hadlers
from handlers.callbacks.handlers_setup import callback_handlers_setup
from handlers.messages.handlers_setup import message_handlers_setup

'''
Start ->
'Make an order' button ->
Web App (Inside the web app all the fun stuff happens) ->
Based on the Web App return (Web App returns status of the shopping, e.g. Customer bought something or Customer didn't) we print the message for user ->
Cycle repeats
'''

async def main():
    message_handlers_setup(router)
    callback_handlers_setup(router)

    bot = Bot(getenv('TOKEN'), parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage()) # ONLY FOR DEVELOPMENT
    if getenv('STORAGE') == 'REDIS':
        redis = Redis(host='127.0.0.1')
        dp = Dispatcher(storage=RedisStorage(redis=redis)) # FOR PRODUCTION
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    load_dotenv
    asyncio.run(main())
