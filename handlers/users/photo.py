from loader import dp
from aiogram.types import Message
from DL_models import nn


@dp.message_handler(content_types=['photo','document'])
async def handle_docs_photo(message: Message):
    try:
        await message.photo[-1].download(message.photo[-1].file_unique_id + ".jpg")
        await message.reply(nn.get_predictions(message.photo[-1].file_unique_id + ".jpg"))
    except Exception as e:
        await message.reply(e)