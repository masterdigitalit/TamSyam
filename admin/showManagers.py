from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.admin import show_managers,count_managers
from keyboard.admin import get_manager_keyboard
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
router = Router()
from db.admin import getAdminsId
from aiogram.filters import BaseFilter, Command
from typing import Union, List
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


@router.message(F.text == "Менеджеры", ChatTypeFilter(getAdminsId()))
async def handle_users_list(message: Message):
    page = 0
    page_size = 5
    users = show_managers(page, page_size)
    total = count_managers()
    total_pages = (total + page_size - 1) // page_size

    if not users:
        await bot.send_message(message.from_user.id, "Нет менеджеров.", reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                    text="Добавить менеджера",
                    callback_data=f"add_manager_admin"
                )]
            ]
        ))

    else:
        keyboard = get_manager_keyboard(users, page)
        text = f"👤 Список менеджеров:\nСтраница {page + 1} из {total_pages}"
        await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("manager_next_"), ChatTypeFilter(getAdminsId()))
async def handle_users_next(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    users = show_managers(page, page_size)
    total = count_managers()
    total_pages = (total + page_size - 1) // page_size

    if not users:
        await callback.answer("Больше пользователей нет.")
        return

    keyboard = get_manager_keyboard(users, page)
    text = f"👤 Список менеджеров:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("manager_prev_"), ChatTypeFilter(getAdminsId()))
async def handle_users_prev(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    users = show_managers(page, page_size)
    total = count_managers()
    total_pages = (total + page_size - 1) // page_size

    keyboard = get_manager_keyboard(users, page)
    text = f"👤 Список менеджеров:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
