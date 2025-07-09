from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import BaseFilter
from typing import Union, List
from create_bot import bot
from db.admin import getAdminsId, get_user_order_stats_all,get_user_order_stats_today
from keyboard.admin import statistic_menu_admin, statistic_menu_next
router = Router()


class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id or []

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.user_ids



@router.message(F.text == "Статистика", ChatTypeFilter(getAdminsId()))
async def handle_orders(message: Message):
    await bot.send_message(message.from_user.id, '📊 За какой период?', reply_markup=statistic_menu_admin())

@router.callback_query(F.data == "stat_menu", ChatTypeFilter(getAdminsId()))
async def handle_orders_all(callback: CallbackQuery):
    await callback.answer()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, '📊 За какой период?', reply_markup=statistic_menu_admin())









@router.callback_query(F.data == "stat_today", ChatTypeFilter(getAdminsId()))
async def handle_today(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)

    stat = get_user_order_stats_today()

    text = (
        "📊 <b>📅 Статистика за <u>сегодня</u></b>\n\n"
        "📦 <b>Заказов выполнено:</b> <code>{count}</code>\n"
        "💰 <b>Прибыль:</b> <code>{total_price} ₽</code>\n"
        "👷‍♂️ <b>Заработали работники:</b> <code>{total_worker_price} ₽</code>\n"
        "🏦 <b>Выручка:</b> <code>{profit} ₽</code>\n"

    ).format(
        count=stat["count"],
        total_price=stat["total_price"],
        total_worker_price=stat["total_worker_price"],
        profit=stat["total_price"] - stat["total_worker_price"],

    )

    await callback.answer()
    await bot.send_message(callback.from_user.id, text, parse_mode="HTML", reply_markup=statistic_menu_next())


@router.callback_query(F.data == "stat_all", ChatTypeFilter(getAdminsId()))
async def handle_all(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    stat = get_user_order_stats_all()

    text = (
        "📊 <b>📅 Статистика за <u>все время</u></b>\n\n"
        "📦 <b>Заказов выполнено:</b> <code>{count}</code>\n"
        "💰 <b>Прибыль:</b> <code>{total_price} ₽</code>\n"
        "👷‍♂️ <b>Заработали работники:</b> <code>{total_worker_price} ₽</code>\n"
        "🏦 <b>Выручка:</b> <code>{profit} ₽</code>\n"

    ).format(
        count=stat["count"],
        total_price=stat["total_price"],
        total_worker_price=stat["total_worker_price"],
        profit=stat["total_price"] - stat["total_worker_price"],

    )

    await callback.answer()
    await bot.send_message(callback.from_user.id, text, parse_mode="HTML", reply_markup=statistic_menu_next())
