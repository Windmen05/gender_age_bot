import random

from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError

from loader import bot, dp, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name) " \
                            "VALUES ($1, $2, $3) RETURNING id"
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"

    async def add_new_user(self):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name
        command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, money, user_id)


db = DBCommands()


@dp.message_handler(commands=["start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    id = await db.add_new_user()
    count_users = await db.count_users()

    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    balance = await db.check_balance()
    text += f"""
Сейчас в базе {count_users} человек!

Ваш баланс: {balance} монет.

Добавить монет: /add_money
"""

    await bot.send_message(chat_id, text)



@dp.message_handler(commands=["add_money"])
async def add_money(message: types.Message):
    random_amount = random.randint(1, 100)
    await db.add_money(random_amount)
    balance = await db.check_balance()

    text = f"""
Вам было добавлено {random_amount} монет.
Теперь ваш баланс: {balance}
    """
    await message.answer(text)
