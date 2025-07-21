from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token='7849310973:AAFrxSDastzpCT62AyI2zFPmJJwpRcFY0rQ')
dp = Dispatcher(bot=bot)