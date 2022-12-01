import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.types import InputFile, InputMediaPhoto

from modules import storer
from modules.db import get_promo

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
if TOKEN:
    bot = Bot(TOKEN)
else:
    print("Define telegram bot token in BOT_TOKEN enviroment variable!")
    exit()

dp = Dispatcher(bot)
USE_STATES = True

CHAT_IDS = (
        -1001626389368,
        -1001872456658,
        )

async def is_user_subscribed(user_id: int) -> bool:
    statuses = {
            (await dp.bot.get_chat_member(chat_id, user_id)).status
            for chat_id in CHAT_IDS
            }
    return bool(statuses & {"member", "creator"}) # intersection

@dp.message_handler(commands=["start"])
async def greeting(message: types.Message):
    storer.new_user(message.from_user.id)
    if not await is_user_subscribed(message.from_user.id):
        await message.answer("Подпишитесь на один из каналов:\nhttps://t.me/sneakerheadsuman\nили https://t.me/sneakerheadsuman\nи нажмите на /start")
        return
    else:
        promo = get_promo(message.from_user.id)
        await message.answer(f"Ваш промокод: `{promo}`", parse_mode="MARKDOWN")


# @dp.message_handler(lambda message: message.text == "Изменить формат поста")
# async def change_post_format(message: types.Message):
#     is_admin = storer.is_user_admin(message.from_user.id)
#     if is_admin:
#         storer.set_user_state(message.from_user.id, "change_post_format")
#         await message.answer("Введите формат")


# @dp.message_handler()
# async def any_message(message: types.Message):
#     is_admin = storer.is_user_admin(message.from_user.id)
#     if is_admin:
#         user_state = storer.get_user_state(message.from_user.id)
#         if user_state == "change_post_format":
#             # insert message to db
#             storer.set_post_format(message.parse_entities())
#             # message of success
#             await message.answer("Успешно!")
#             # state none
#             storer.set_user_state(message.from_user.id, "none")
#         elif user_state == "change_sale_post_format":
#             # insert message to db
#             storer.set_sale_post_format(message.parse_entities())
#             # message of success
#             await message.answer("Успешно!")
#             # state none
#             storer.set_user_state(message.from_user.id, "none")
#         elif user_state == "change_prepost_message":
#             # insert message to db
#             storer.set_prepost_info(caption=message.parse_entities(), photo="pictures/prepost.png")
#             # message of success
#             await message.answer("Успешно!")
#             # state none
#             storer.set_user_state(message.from_user.id, "none")
#         elif user_state == "change_prepost_photo_dbg":
#             # insert message to db
#             await message.photo[0].download("pictures/prepost.png")
#             # message of success
#             await message.answer("Успешно!")
#             # state none
#             storer.set_user_state(message.from_user.id, "none")


if __name__ == "__main__":
    # executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp)

