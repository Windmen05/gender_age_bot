from aiogram import types
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from aiogram.types import Message
from loader import bot, dp, db
from DL_models import nn, face_detection
from numpy import array
import cv2
import os
from PIL import Image
import io

class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    SELECT_PREDS = "SELECT COUNT(*) FROM user_preds"
    SELECT_ALL_PREDS = "SELECT pred_chance, file_unique_id, pred_sex, id FROM user_preds"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    ADD_PRED = "INSERT INTO user_preds(chat_id, file_unique_id, pred_chance, pred_sex) " \
               "VALUES ($1, $2, $3, $4) RETURNING id"

    # CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    # ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"

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

    async def count_preds(self):
        record: Record = await self.pool.fetchval(self.SELECT_PREDS)
        return record

    async def show_all_preds(self):
        record: Record = await self.pool.fetch(self.SELECT_ALL_PREDS)
        return record
        #test = await self.pool.fetchrow(self.SELECT_ALL_PREDS)
        #return test

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def add_pred(self, file_unique_id, pred_chance, pred_sex):
        command = self.ADD_PRED
        user_id = types.User.get_current().id

        return await self.pool.fetchval(command, user_id, file_unique_id, pred_chance, pred_sex)

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

    # balance = await db.check_balance()
    text += f"""
Сейчас в базе {count_users} человек!
"""

    await bot.send_message(chat_id, text)

'''
@dp.message_handler(content_types=['photo', 'document'])
async def handle_docs_photo(message: Message):
    try:
        chat_id = message.from_user.id
        unique_id = message.photo[-1].file_unique_id
        downloaded = await bot.download_file_by_id(message.photo[-1].file_id)
        male, pred = nn.get_predictions(downloaded.getvalue())
        await db.add_pred(unique_id, pred, male)
        await message.reply((int(1 - male) * 'fe' + 'male with chanse: ') + str(pred) + "%")
    except Exception as e:
        await message.reply(e)
        raise IOError(e)
'''


###Process photo without save on disk // bytes
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: Message):
    try:
        downloaded = await bot.download_file_by_id(message.photo[-1].file_id)
        text = 'test_text'
        img = face_detection.get_predictions(downloaded.getvalue(), text)
        is_success, img_buf_arr = cv2.imencode(".jpg", img)
        byte_img = img_buf_arr.tobytes()
        await message.answer_photo(photo=byte_img)
    except Exception as e:
        raise IOError(e)
        await message.reply(e)


@dp.message_handler(commands=["show_all_preds"])
async def handle_docs_photo(message: Message):
    chat_id = message.from_user.id
    count_users = await db.show_all_preds()
    count_preds = await db.count_preds()
    text = f"""You predicted {count_preds} images
    """
    for i in count_users:
        pred_text = (int(1 - i['pred_sex']) * 'fe' + 'male with chanse: ' + str(i['pred_chance']) + "%")
        text += \
        f"""
        file with unique id = {i['file_unique_id']} 
        and id = {i['id']} was predicted as {pred_text}
        """
    await bot.send_message(text=text, chat_id=chat_id)
#pred_chance, file_unique_id, pred_sex, id