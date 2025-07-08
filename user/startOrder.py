from aiogram import Router, F
from aiogram.types import Message
from create_bot import bot
from db.user import getOrder, setOrderActive, count_user_orders
from keyboard.user import back_to_orders_button
from aiogram.types import CallbackQuery
router = Router()

@router.callback_query(F.data.startswith("start_"))
async def handle_start_order(callback: CallbackQuery):
    try:
        order_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.answer("Ошибка: не удалось получить ID заказа.")
        return

    row = getOrder(order_id)
    active_orders = count_user_orders(callback.from_user.id)


    if not row:
        await callback.answer("Заказ не найден.")
        return

    if row['Active'] == 1:
        await callback.answer("Этот заказ уже активен.")
        return
    if active_orders != 0:
        await callback.answer("Вы не можете взять несколько заказов одноврменно")
        return


    setOrderActive( callback.from_user.id, order_id)

    await callback.answer("🚀 Вы приступили к заказу!")
    await callback.message.edit_text(f"✅ Заказ #{order_id} отмечен как активный.")
