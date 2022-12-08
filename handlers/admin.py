from aiogram.dispatcher import FSMContext, Dispatcher
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import dp, bot
from aiogram.dispatcher.filters import Text
from data_base import sqlite_db
from keyboards import admin_cb
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
ADMIN_ID = [1760676377]
MAIN_ADMIN = 1760676377

class FSMadmin2(StatesGroup):
    admin = State()

class FSMadmin3(StatesGroup):
    admin = State()

class FSMadmin(StatesGroup):
    photo = State()
    name = State()
    info = State()
    time = State()


async def make_changes_command(message: types.Message):

    global MAIN_ADMIN
    await bot.send_message(message.from_user.id, 'какие хотите добавить обновления?',reply_markup=admin_cb.button_case_admin)


async def cm_start(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        await FSMadmin.photo.set()
        await message.reply('Загрузи фото администратора')

async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMadmin.next()
        await message.reply('Теперь введи имя администратора')

async def load_name(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMIN_ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMadmin.next()
        await message.reply('Теперь введи информацию об администраторе')

async def load_info(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMIN_ID:
        async with state.proxy() as data:
            data['info'] = message.text
        await FSMadmin.next()
        await message.reply('Теперь введи время работы администратора')

async def load_time(message: types.Message, state:FSMContext):
    if message.from_user.id in ADMIN_ID:
        async with state.proxy() as data:
            data['time'] = message.text
        await sqlite_db.sql_add_command(state)

        await state.finish()

async def cancel_handlers_admin(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMIN_ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ',''))
    await callback_query.answer(text=f'{callback_query.data.replace("del", "")} удалена.', show_alert=True)


async def delete_item(message: types.Message):
    if message.from_user.id in ADMIN_ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\n Информация: {ret[2]} \n Время: {ret[3]}')
            await bot.send_message(message.from_user.id, text='Вы хотите удалить эту запись ^', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить {ret[1]}',callback_data=f'del {ret[1]}')))


@dp.message_handler(commands='newadmin')
async def phrase1(message: types.Message):
    if message.from_user.id == MAIN_ADMIN:
        await FSMadmin2.admin.set()
        await bot.send_message(message.from_user.id,'Ведите айди нового администратора  в форме целого числа без каких либо других символов')
      
@dp.message_handler(state=FSMadmin2.admin)
async def g_admin(message: types.Message,  state:FSMContext):
    if message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['admin'] = message.text
        if message.text.isdigit() == True:
            ADMIN_ID.append(int(message.text))
            await bot.send_message(message.from_user.id,'вы успешно добавили администратора')
        else:
            await state.finish()


@dp.message_handler(commands='deladmin')
async def del_admin(message: types.Message):
    if message.from_user.id == MAIN_ADMIN:
        await FSMadmin3.admin.set()
        await bot.send_message(message.from_user.id,'Ведите айди администратора, кого хотите удалить')

@dp.message_handler(state=FSMadmin3.admin)
async def d_admin(message:types.Message, state:FSMContext):
    if message.from_user.id == MAIN_ADMIN:
        async with state.proxy() as data:
            data['admin'] = message.text
        if message.text.isdigit() == True:
            if int(message.text) in ADMIN_ID:
                ADMIN_ID.remove(int(message.text))
                await bot.send_message(message.from_user.id, 'Вы успешно удалили администратора')
            else: 
                await bot.send_message(message.from_user.id, 'такого айди админа не существует')
        else:
            await state.finish()

@dp.message_handler(state='*',commands='отмена')
@dp.message_handler(Text(equals = 'отмена', ignore_case=True),state='*')
async def cancel_handlers(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(make_changes_command, commands=['moderator'] )
    dp.register_message_handler(cm_start, text='Загрузить', state=None)
    dp.register_message_handler(load_photo, content_types=['photo'],state=FSMadmin.photo)
    dp.register_message_handler(load_name,state=FSMadmin.name)
    dp.register_message_handler(load_info,state=FSMadmin.info)
    dp.register_message_handler(load_time,state=FSMadmin.time)
    dp.register_message_handler(delete_item, text='Удалить')