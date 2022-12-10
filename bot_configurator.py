import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from aiogram.types import InputFile, InputMediaPhoto

from modules import storer
from modules.db import set_refresh_all
from keyboards import start_keyboard

load_dotenv()

TOKEN = os.getenv("ADMIN_BOT_TOKEN")
if TOKEN:
    bot = Bot(TOKEN)
else:
    print("Define telegram bot token in BOT_TOKEN enviroment variable!")
    exit()

dp = Dispatcher(bot)
USE_STATES = True


@dp.message_handler(commands=["start"])
async def greeting(message: types.Message):
    storer.new_user(message.from_user.id)
    args = message.get_args()
    if args:
        if args == os.getenv("ADMINCODE"):
            storer.add_admin(message.from_user.id)
            await message.answer("Вы стали админом бота")
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        await message.answer("Приветствую", reply_markup=start_keyboard)

@dp.message_handler(commands=["refresh_all"])
async def refresh(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        set_refresh_all(True)
        await message.answer("Процесс начат...", reply_markup=start_keyboard)

@dp.message_handler(commands=["renew_sale"])
async def renew_sale(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        storer.set_renew_flag(True)
        await message.answer("Процесс начат...", reply_markup=start_keyboard)

@dp.message_handler(commands=["update_prepost"])
async def update_post(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        prepost = storer.get_prepost_info()
        for chat_id, message_id in storer.get_preposts():
            photo_media = InputMediaPhoto(InputFile(prepost.photo), caption=prepost.caption)
            await bot.edit_message_media(photo_media, chat_id, message_id)

@dp.message_handler(lambda message: message.text == "Изменить формат поста")
async def change_post_format(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        storer.set_user_state(message.from_user.id, "change_post_format")
        await message.answer("Введите формат")

@dp.message_handler(lambda message: message.text == "Изменить текст препоста")
async def change_prepost_message(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        storer.set_user_state(message.from_user.id, "change_prepost_message")
        await message.answer("Введите сообщение")

@dp.message_handler(lambda message: message.text == "Изменить картинку препоста")
async def change_prepost_photo(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        storer.set_user_state(message.from_user.id, "change_prepost_photo")
        await message.answer("Отправте картинку или ссылку")

@dp.message_handler(lambda message: message.text == "Изменить формат акционного поста")
async def change_sale_post_format(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        storer.set_user_state(message.from_user.id, "change_sale_post_format")
        await message.answer("Введите формат")

@dp.message_handler(lambda message: message.text == "Текущий формат")
async def get_post_format(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        post_format = storer.get_post_format()
        await message.answer(post_format, parse_mode="HTML")

@dp.message_handler(lambda message: message.text == "Текущий формат акционного поста")
async def get_sale_post_format(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        post_format = storer.get_sale_post_format()
        await message.answer(post_format, parse_mode="HTML")

@dp.message_handler(lambda message: message.text == "Возможные поля")
async def get_format_fields(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        msg = (
                "{name} - наименование товара\n"
                "{price} - цена товара в долларах\n"
                "{description} - описание товара\n"
                "{sizes} - размеры товара\n"
                "{tags} - теги товара\n"
                "{product_url} - ссылка на товар\n"
                "{order_url} - ссылка на заказ товара\n"
                "Для акционного поста:\n"
                "{new_price} - цена по акции\n"
                "{date} - дата текущего поста\n"
                )
        await message.answer(msg)

@dp.message_handler()
async def any_message(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        user_state = storer.get_user_state(message.from_user.id)
        if user_state == "change_post_format":
            # insert message to db
            storer.set_post_format(message.parse_entities())
            # message of success
            await message.answer("Успешно!")
            # state none
            storer.set_user_state(message.from_user.id, "none")
        elif user_state == "change_sale_post_format":
            # insert message to db
            storer.set_sale_post_format(message.parse_entities())
            # message of success
            await message.answer("Успешно!")
            # state none
            storer.set_user_state(message.from_user.id, "none")
        elif user_state == "change_prepost_message":
            # insert message to db
            storer.set_prepost_info(caption=message.parse_entities(), photo="pictures/prepost.png")
            # message of success
            await message.answer("Успешно!")
            # state none
            storer.set_user_state(message.from_user.id, "none")
        elif user_state == "change_prepost_photo":
            url = message.text
            storer.set_prepost_info(photo=url, is_photo_file=False)
            await message.answer("Успешно!")
            # state none
            storer.set_user_state(message.from_user.id, "none")
        # else:
        #     print(message.parse_entities())
        #     await message.answer(message.parse_entities(), parse_mode="HTML")

@dp.message_handler(content_types=["photo"])
async def photo_message(message: types.Message):
    is_admin = storer.is_user_admin(message.from_user.id)
    if is_admin:
        user_state = storer.get_user_state(message.from_user.id)
        if user_state == "change_prepost_photo":
            # insert message to db
            print(message.photo)
            await message.photo[-1].download("pictures/prepost.png")
            storer.set_prepost_info(photo="pictures/prepost.png", is_photo_file=True)
            # message of success
            await message.answer("Успешно!")
            # state none
            storer.set_user_state(message.from_user.id, "none")

@dp.chat_member_handler()
async def some(m):
    print(m)
    print(dir(m))


if __name__ == "__main__":
    # executor.start_polling(dp, skip_updates=True)
    executor.start_polling(dp)

