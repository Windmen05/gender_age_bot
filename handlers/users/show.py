from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text


@dp.message_handler(Command("show_all"))
async def show_menu(message: Message):
    await message.answer("Выберите кнопку", reply_markup=menu)

