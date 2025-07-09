from aiogram import Router, F

from db.user import getOrder
from keyboard.user import back_to_orders_button, back_to_my_orders_button
from aiogram.types import CallbackQuery
router = Router()

@router.callback_query(F.data.startswith("order_"))
async def handle_order_detail(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[1])

    row = getOrder(order_id)

    if row is None:
        await callback.answer("Такой заказ не найден.")
        return
    if row['Active']:


        order = dict(row)
        text = (
            f"📝 Детали заказа #{order['Id']}:\n\n"
            f"📍 Адрес: {order['Adress']}\n"
            f"👤 Клиент: {order['FullName']}\n"
            f"📞 Телефон: {order['Phone']}\n"
            f"✅ Активный: {'Да' if order['Active'] else 'Нет'}"
        )
        page = 0
        await callback.message.edit_text(text, reply_markup=back_to_my_orders_button(page, order_id))
        await callback.answer()
    else:
        order = dict(row)
        text = (
            f"📝 Детали заказа #{order['Id']}:\n\n"
            f"📍 Адрес: {order['Adress']}\n"
            f"👤 Клиент: {order['FullName']}\n"
            f"📞 Телефон: {order['Phone']}\n"
            f"✅ Активный: {'Да' if order['Active'] else 'Нет'}"
        )
        page = 0
        await callback.message.edit_text(text, reply_markup=back_to_orders_button(page, order_id))
        await callback.answer()
