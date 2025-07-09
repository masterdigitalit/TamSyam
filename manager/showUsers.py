from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from db.manager import show_workers, count_user_orders
from keyboard.manager import get_manager_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import bot
router = Router()
from typing import Union, List
from aiogram.filters import BaseFilter, Command
from aiogram.types import Message
from db.manager import getManagersId


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





@router.message(F.text == "Работники", ChatTypeFilter(getManagersId()))
async def handle_users_list(message: Message):
    page = 0
    page_size = 5
    users = show_workers(page, page_size)
    total = count_user_orders()
    total_pages = (total + page_size - 1) // page_size

    if not users:
        await bot.send_message(message.from_user.id, "Нет пользователей.",  reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(
                text="Добавить работника",
                callback_data=f"add_user"
            )]
            ]
        ))
    else:
        keyboard = get_manager_keyboard(users, page)
        text = f"👤 Список работников:\nСтраница {page + 1} из {total_pages}"
        await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("user_next_"), ChatTypeFilter(getManagersId()))
async def handle_users_next(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    users = show_workers(page, page_size)
    total = count_user_orders()
    total_pages = (total + page_size - 1) // page_size

    if not users:
        await callback.answer("Больше пользователей нет.")
        return

    keyboard = get_manager_keyboard(users, page)
    text = f"👤 Список работников:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("user_prev_"), ChatTypeFilter(getManagersId()))
async def handle_users_prev(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    users = show_workers(page, page_size)
    total = count_user_orders()
    total_pages = (total + page_size - 1) // page_size

    keyboard = get_manager_keyboard(users, page)
    text = f"👤 Список работников:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
