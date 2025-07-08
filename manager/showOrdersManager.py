from aiogram import Router, F
from aiogram.types import Message
from create_bot import bot
from db.manager import get_orders, count_orders
from keyboard.manager import get_orders_keyboard
from aiogram.types import CallbackQuery
from typing import Union, List
from aiogram.filters import BaseFilter, Command
from db.manager import getManagersId

router = Router()



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




@router.message(F.text == "Заказы", ChatTypeFilter(getManagersId()))
async def handle_orders(message: Message):
    page = 0
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    if total_orders == 0:
        text = f"📦 Доступных заказов нет"
        await message.answer(text)
    else:

        total_pages = (total_orders + page_size - 1) // page_size

        keyboard = get_orders_keyboard(orders, page)
        text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
        await message.answer(text, reply_markup=keyboard)




@router.callback_query(F.data.startswith("next_manager_"), ChatTypeFilter(getManagersId()))
async def handle_next_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    total_pages = (total_orders + page_size - 1) // page_size

    if not orders:
        await callback.answer("Больше заказов нет.")
        return

    keyboard = get_orders_keyboard(orders, page)
    text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("prev_manager_"), ChatTypeFilter(getManagersId()))
async def handle_prev_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    total_pages = (total_orders + page_size - 1) // page_size

    keyboard = get_orders_keyboard(orders, page)
    text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("page_manager_"), ChatTypeFilter(getManagersId()))
async def handle_back_to_orders(callback: CallbackQuery):
    page = int(callback.data.split("_")[2])
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    total_pages = (total_orders + page_size - 1) // page_size

    keyboard = get_orders_keyboard(orders, page)
    text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
