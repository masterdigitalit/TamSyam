from aiogram import Router
from create_bot import bot
from keyboard.admin import main_menu_admin
router = Router()
from db.admin import getAdminsId
from aiogram.filters import BaseFilter, Command
from typing import Union, List

from aiogram.types import Message
# Фильтр
class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        if isinstance(user_id, int):
            self.user_ids = [user_id]
        else:
            self.user_ids = user_id or []

    async def __call__(self, message: Message) -> bool:

        print(f"[FILTER] from_user.id = {message.from_user.id}")
        print(f"[FILTER] self.user_ids = {self.user_ids}")

        if not self.user_ids:
            return False
        return message.from_user.id in self.user_ids


@router.message(Command("start"), ChatTypeFilter(getAdminsId()))
async def admin_start_handler(message: Message):
    await bot.send_message(message.chat.id, "Привет, админ!\nЧто хочешь сделать ?", reply_markup=main_menu_admin())