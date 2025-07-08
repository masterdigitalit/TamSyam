from aiogram import Router, F
from aiogram.types import Message
from db.user import get_user_done_paid_orders, get_user_done_not_paid_orders
router = Router()
@router.message(F.text.lower() == "баланс")
async def handle_balance(message: Message):
    user_id = message.from_user.id
    print(user_id)
    paidBalance = get_user_done_paid_orders(user_id)
    waitToPay = get_user_done_not_paid_orders(user_id)
    await message.answer(f"""
💰 Выплачено: <b>{paidBalance}₽</b>\n
💰 Ожидает оплаты: <b>{waitToPay}₽</b>

        """, parse_mode="HTML")
