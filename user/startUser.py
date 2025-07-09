from typing import Union, List
from aiogram.filters import BaseFilter, Command
from aiogram.types import Message
from aiogram import Router
from db.user import getUsersId
from create_bot import bot
from keyboard.user import main_menu_worker
router = Router()



@router.message(Command("start"))
async def no_access_handler(message: Message):
    print(getUsersId())
    if message.from_user.id not in getUsersId():
        await bot.send_message(message.chat.id, "Привет,прости , но тебя нет в списках , напиши админу @work_minister")
    else:
        await bot.send_message(message.chat.id, "Привет, работник!", reply_markup=main_menu_worker())
