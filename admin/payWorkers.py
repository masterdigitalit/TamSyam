from aiogram import Router, F
from aiogram.types import CallbackQuery
from create_bot import bot
from db.admin import get_unpaid_workers_paginated, count_unpaid_workers, get_order_to_pay, set_order_paid
from keyboard.admin import get_pay_workers_keyboard, pay_to_worker_confirm_btn
from aiogram.filters import BaseFilter
from typing import Union, List
from db.admin import getAdminsId

router = Router()


# Фильтр админов
class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id or []

    async def __call__(self, message) -> bool:
        return message.from_user.id in self.user_ids


# 🔘 Старт — показать первую страницу
@router.callback_query(F.data == "pay_workers", ChatTypeFilter(getAdminsId()))
async def show_pay_workers(callback: CallbackQuery):
    page = 0
    page_size = 10
    orders = get_unpaid_workers_paginated(offset=page * page_size, limit=page_size)
    total_orders = count_unpaid_workers()

    if not orders:
        await callback.answer("Нет работников, ожидающих оплату.")
        return

    total_pages = (total_orders + page_size - 1) // page_size
    text = f"💸 <b>Работники, ожидающие оплату:</b>\nСтраница {page + 1} из {total_pages}"
    markup = get_pay_workers_keyboard(orders, page)

    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()


# 🔁 Следующая страница
@router.callback_query(F.data.startswith("pay_worker_next_"), ChatTypeFilter(getAdminsId()))
async def handle_next_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[3])
    page_size = 10
    orders = get_unpaid_workers_paginated(offset=page * page_size, limit=page_size)

    total_orders = count_unpaid_workers()
    total_pages = (total_orders + page_size - 1) // page_size

    if not orders:
        await callback.answer("Это последняя страница.")
        return

    markup = get_pay_workers_keyboard(orders, page)
    text = f"💸 <b>Работники, ожидающие оплату:</b>\nСтраница {page + 1} из {total_pages}"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()


# 🔁 Предыдущая страница
@router.callback_query(F.data.startswith("pay_worker_prev_"), ChatTypeFilter(getAdminsId()))
async def handle_prev_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[3])
    page_size = 10
    orders = get_unpaid_workers_paginated(offset=page * page_size, limit=page_size)
    total_orders = count_unpaid_workers()
    total_pages = (total_orders + page_size - 1) // page_size

    markup = get_pay_workers_keyboard(orders, page)
    text = f"💸 <b>Работники, ожидающие оплату:</b>\nСтраница {page + 1} из {total_pages}"

    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()


# ✅ Обработка выбора работника
@router.callback_query(F.data.startswith("pay_worker_"), ChatTypeFilter(getAdminsId()))
async def handle_worker_payment(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) != 3 or not parts[2].isdigit():
        await callback.answer("Некорректные данные", show_alert=True)
        return

    order_id = int(parts[2])
    order = get_order_to_pay(order_id)
    print(order, order_id)

    # Получаем заказ


    if not order:
        await callback.answer("Заказ не найден или уже оплачен", show_alert=True)
        return

    text = (
        f"<b>📦 Заказ №{order['Id']}</b>\n\n"
        f"<b>👷 Работник:</b> {order['WorkerName'] or 'Неизвестен'}\n"
        f"<b>🆔 Telegram ID:</b> <code>{order['WorkerId']}</code>\n"
        f"<b>📍 Адрес:</b> {order['Adress']}\n"
        f"<b>📅 Дата создания:</b> {order['dateCreated']}\n"
        f"<b>💰 К выплате:</b> <code>{order['WorkerPrice']} ₽</code>"
    )

    markup = pay_to_worker_confirm_btn(order)
    await callback.message.answer(text, parse_mode="HTML", reply_markup=markup)
    await callback.answer()


@router.callback_query(F.data.startswith("pay_to_user_order_admin_confirm_"), ChatTypeFilter(getAdminsId()))
async def confirm_worker_payment(callback: CallbackQuery):
    parts = callback.data.split("_")
    if len(parts) < 6 or not parts[-1].isdigit():
        await callback.answer("❌ Некорректные данные", show_alert=True)
        return

    order_id = int(parts[-1])

    # Проверяем заказ
    order = get_order_to_pay(order_id)
    if not order:
        await callback.answer("⚠️ Заказ не найден или уже оплачен", show_alert=True)
        return

    # Обновляем статус оплаты в БД
    set_order_paid(order_id)

    # Удаляем кнопки и сообщаем об оплате
    await callback.message.edit_text(
        f"✅ Выплата <b>{order['WorkerPrice']} ₽</b> работнику <b>{order['WorkerName']}</b> подтверждена.",
        parse_mode="HTML"
    )
    await callback.answer("💸 Выплата прошла успешно")
