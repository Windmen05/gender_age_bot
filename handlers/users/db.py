import cv2
from aiogram import types
from aiogram.types import Message
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from DL_models import models_predict
from loader import bot, dp, db


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    SELECT_PREDS = "SELECT COUNT(*) FROM user_preds"
    SELECT_ALL_PREDS = "SELECT pred_chance, file_unique_id, pred_sex, id, pred_age FROM user_preds"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    ADD_PRED = "INSERT INTO user_preds(chat_id, file_unique_id, pred_chance, pred_sex, pred_age) " \
               "VALUES ($1, $2, $3, $4, $5) RETURNING id"

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

    async def add_pred(self, file_unique_id, pred_chance, pred_sex, pred_age):
        command = self.ADD_PRED
        user_id = types.User.get_current().id

        return await self.pool.fetchval(command, user_id, file_unique_id, pred_chance, pred_sex, pred_age)

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


###Process photo without save on disk // bytes
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: Message):
    try:
        unique_id = message.photo[-1].file_unique_id
        downloaded = await bot.download_file_by_id(message.photo[-1].file_id)

        img, preds_sex_chance, preds_sex, preds_age = models_predict.get_predictions(downloaded.getvalue())

        for i in range(preds_sex.shape[0]):
            await db.add_pred(unique_id, preds_sex_chance[i], bool(preds_sex[i]), preds_age[i])

        is_success, img_buf_arr = cv2.imencode(".jpg", img)
        byte_img = img_buf_arr.tobytes()

        await message.answer_photo(photo=byte_img)
    except UnboundLocalError:
        await message.reply("face not recognized, please upload another photo")
    except Exception as e:
        #raise IOError(e)
        await message.reply(e)


@dp.message_handler(commands=["show_all_preds"])
async def handle_docs_photo(message: Message):
    chat_id = message.from_user.id
    count_users = await db.show_all_preds()
    count_preds = await db.count_preds()
    text = f"""You predicted {count_preds} images
    """
    for i in count_users:
        pred_text = (int(1 - i['pred_sex']) * 'fe' + 'male with chanse: ' + str(i['pred_chance'])
                     + "% \n and age: "+ str(float(i['pred_age'])/10))
        text += \
        f"""
        file with unique id = {i['file_unique_id']} 
        and id = {i['id']} was predicted as {pred_text}
        """
    await bot.send_message(text=text, chat_id=chat_id)