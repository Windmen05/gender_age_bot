'''from loader import dp
from aiogram.types import Message
from DL_models import nn
from time import time
import numpy as np

@dp.message_handler(content_types=['photo','document'])
async def handle_docs_photo(message: Message):
    await message.reply(message.chat.id)
    await dp.bot.send_message(text="Привет", reply_to_message_id=621, chat_id=279418443)'''