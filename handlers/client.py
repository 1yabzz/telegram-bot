from aiogram import types, Dispatcher
from config import bot, dp
from keyboards import kb_client 
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMINS_ID = 1760676377

kb = InlineKeyboardMarkup(row_width=2)
Button = InlineKeyboardButton(text='Записаться на сессию самокат', callback_data='самокат')
Button2 = InlineKeyboardButton(text='Записаться на сессию BMX', callback_data='велосипед')
kb.row(Button).row(Button2)


async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,'Привет, это телеграм бот лучшего скейтпарка на свете Slavyanskiy training', reply_markup=kb_client)

async def history_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здесь будет история славянского тренинга')

async def place_command(message: types.Message):
    await bot.send_message(message.from_user.id,'г.Орск проспект мира 26а, бывший зал греко-римской борьбы')

async def questions_command(message: types.Message):
    await bot.send_message(message.from_user.id,'тут будут вопросы про парк которые чаще всего задают')

async def enroll_command(message: types.Message):
    read = await sqlite_db.sql_read2()
    for ret in read:
        await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Информация: {ret[2]} \n Время: {ret[3]}')
        await bot.send_message(message.from_user.id, text='Вы хотите записаться на сессию', reply_markup=kb)

@dp.callback_query_handler(text='самокат')
async def sendi(callback : types.CallbackQuery ):
    global ADMINS_ID
    await bot.send_message(ADMINS_ID,'на сессию записался 1 человек на самокате')
    await callback.answer('Вы записались на сессию на самокате')

@dp.callback_query_handler(text='велосипед')
async def sendi(callback : types.CallbackQuery ):
    global ADMINS_ID
    await bot.send_message(ADMINS_ID,'на сессию записался 1 человек на велосипеде')
    await callback.answer('Вы записались на сессию на BMX')

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler (command_start, commands=['start','help'])
    dp.register_message_handler (history_command, text='Наша история')
    dp.register_message_handler (place_command, text='Расположение')
    dp.register_message_handler (questions_command, text='Часто задаваемые вопросы')
    dp.register_message_handler (enroll_command, text="Записаться на сессию")