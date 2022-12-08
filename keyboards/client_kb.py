from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('Наша история')
b2 = KeyboardButton('Расположение')
b3 = KeyboardButton('Часто задаваемые вопросы')
b4 = KeyboardButton('Записаться на сессию')

kb_client= ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)

kb_client.add(b1).add(b2).add(b3).add(b4)