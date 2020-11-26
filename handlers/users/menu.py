from loader import dp
from aiogram.types import Message, ReplyKeyboardRemove
from keyboards.default import menu
from aiogram.dispatcher.filters import Command, Text


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите кнопку", reply_markup=menu)


@dp.message_handler(Text(equals=["test1", "test2", "test3"]))
async def test_answer(message: Message):
    await message.answer(f"Вы выбрали {message.text}. Спасибо", reply_markup=ReplyKeyboardRemove())

