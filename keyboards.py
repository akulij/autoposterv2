from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add("Изменить формат поста")
start_keyboard.add("Изменить формат акционного поста")
start_keyboard.add("Изменить текст препоста")
start_keyboard.add("Изменить картинку препоста")
start_keyboard.add("Текущий формат")
start_keyboard.add("Текущий формат акционного поста")
start_keyboard.add("Возможные поля")
