from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage=MemoryStorage()

BOT_TOKEN = '5704852188:AAGklMB0nuF8EGBWudN2c6cGPqtOf3QTOYY'

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)
