from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="test1")
        ],
        [
            KeyboardButton(text="test2"),
            KeyboardButton(text="test3")
        ],
    ],
    resize_keyboard=True
)