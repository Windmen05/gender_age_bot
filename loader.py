import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data.config import BOT_TOKEN

import logging
from sql import create_pool, create_db

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)
loop = asyncio.get_event_loop()

# Set up storage (either in Redis or Memory)
storage = MemoryStorage()
# storage = RedisStorage2()

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage, loop=loop)

db = dp.loop.run_until_complete(create_pool())
