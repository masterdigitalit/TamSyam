from aiogram import Router, F
from aiogram.types import (
    Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from typing import Union, List
from aiogram.filters import BaseFilter
from db.manager import (
    getOrder, getOrderWorker,
    deleteOrderById, getManagersId
)
from create_bot import bot

router = Router()

# ======= Фильтр по ID менеджеров =======
class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        if isinstance(user_id, int):
            self.user_ids = [user_id]
        else:
            self.user_ids = user_id or []

    async def __call__(self, message: Message) -> bool:
        print(f"[FILTER] from_user.id = {message.from_user.id}")
        print(f"[FILTER] self.user_ids = {self.user_ids}")
        return message.from_user.id in self.user_ids

# ======= Кнопка "Назад к заказам" и Удалить =======
def back_to_orders_button(page: int = 0, order_id: int = 0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="⬅ Назад к заказам", callback_data=f"page_manager_{page}"),
                InlineKeyboardButton(text="🗑 Удалить", callback_data=f"order_confirm_remove_{order_id}")
            ]
        ]
    )

# ======= Просмотр деталей заказа =======
@router.callback_query(F.data.startswith("order_manage_"), ChatTypeFilter(getManagersId()))
async def handle_order_detail(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[2])
    row = getOrder(order_id)

    if row is None:
        await callback.answer("❌ Такой заказ не найден.")
        return

    order = dict(row)
    page = 0
    print(order)

    if order['Done']:
        worker_list = getOrderWorker(order['WorkerId'])
        worker = worker_list[0] if worker_list else {"UserName": "-", "Name": "-"}

        text = (
            f"📝 Детали заказа #{order['Id']}:\n\n"
            f"📍 Адрес: {order['Adress']}\n"
            f"👤 Клиент: {order['FullName']}\n"
            f"📞 Телефон: {order['Phone']}\n"
            f"✅ Активный: Да\n"
            f"👷 Дата создания: {order['dateCreated']}\n"
            f"👷 Дата вступления в работу: {order['dateStarted']}\n"
            f"👷 Дата окончания: {order['dateDone']}\n"
            f"💲 Цена: {order['Price']}\n"

        )

    elif order['Active']:
        worker_list = getOrderWorker(order['WorkerId'])
        worker = worker_list[0] if worker_list else {"UserName": "-", "Name": "-"}
        text = (
            f"📝 Детали заказа #{order['Id']}:\n\n"
            f"📍 Адрес: {order['Adress']}\n"
            f"👤 Клиент: {order['FullName']}\n"
            f"📞 Телефон: {order['Phone']}\n"
            f"✅ Активный: Да\n"
            f"👷 Дата создания: {order['dateCreated']}\n"
            f"👷 Дата вступления в работу: {order['dateStarted']}\n"

        )
    else:
        text = (
            f"📝 Детали заказа #{order['Id']}:\n\n"
            f"📍 Адрес: {order['Adress']}\n"
            f"👤 Клиент: {order['FullName']}\n"
            f"📞 Телефон: {order['Phone']}\n"
            f"✅ Активный: Нет\n"
        f"👷 Дата создания: {order['dateCreated']}"
        )

    await callback.message.edit_text(text, reply_markup=back_to_orders_button(page, order_id))
    await callback.answer()

# ======= Подтверждение удаления =======
@router.callback_query(F.data.startswith("order_confirm_remove_"), ChatTypeFilter(getManagersId()))
async def confirm_order_delete(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[-1])
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"order_manager_remove_{order_id}"),
            InlineKeyboardButton(text="❌ Нет", callback_data=f"cancel_order_delete_{order_id}")
        ]
    ])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        f"❗ Вы уверены, что хотите удалить заказ #{order_id}?",
        reply_markup=kb
    )
    await callback.answer()

# ======= Отмена удаления =======
@router.callback_query(F.data.startswith("cancel_order_delete_"), ChatTypeFilter(getManagersId()))
async def cancel_delete_order(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[-1])
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer("❌ Удаление отменено.")
    await callback.answer()

# ======= Удаление заказа =======
@router.callback_query(F.data.startswith("order_manager_remove_"), ChatTypeFilter(getManagersId()))
async def handle_order_delete(callback: CallbackQuery):
    try:
        order_id = int(callback.data.split("_")[-1])
    except ValueError:
        await callback.answer("❌ Неверный ID заказа.", show_alert=True)
        return

    success = deleteOrderById(order_id)

    if success:
        await callback.message.edit_text(
            text=f"🗑 Заказ <code>#{order_id}</code> успешно удалён.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="⬅ Назад к заказам", callback_data="page_manager_0")]
                ]
            )
        )
    else:
        await callback.answer("❌ Не удалось удалить заказ.", show_alert=True)
