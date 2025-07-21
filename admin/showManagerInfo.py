from aiogram import Router, F
from aiogram.types import CallbackQuery
from db.admin import get_user_by_id
from keyboard.admin import back_to_managers_button
from db.admin import getOwnersId
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



        if not self.user_ids:
            return False
        return message.from_user.id in self.user_ids



router = Router()

@router.callback_query(F.data.startswith("manager_"), ChatTypeFilter(getOwnersId()))
async def handle_user_detail(callback: CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный ID пользователя.")
        return

    manager = get_user_by_id(user_id)


    if not manager:
        await callback.answer("Пользователь не найден.")
        return



    text = (
        f"👤 <b>Профиль менеджера</b>\n\n"
        f"🆔 ID: <code>{manager['Id']}</code>\n"
        f"📛 Имя: <b>{manager['Name']}</b>\n"
        # f"📞 Телефон: <code>{user['Phone']}</code>\n\n"
      f"Тг @{manager['UserName']}"
    )


    keyboard = back_to_managers_button(id=manager['TelegramId'])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
