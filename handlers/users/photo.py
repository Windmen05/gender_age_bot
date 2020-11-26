from loader import dp
from aiogram.types import Message


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: Message):
    try:
        await message.photo[-1].download("/home/vadim/Downloads/" + 'test.jpg')
        await message.reply("Спасибо, сохранил")
    except Exception as e:
        dp.reply_to(message, e)
