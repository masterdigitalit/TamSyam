from aiogram import Router, F
from aiogram.types import Message
from db.user import get_user_done_paid_orders
router = Router()
@router.message(F.text.lower() == "баланс")
async def handle_balance(message: Message):
    user_id = message.from_user.id
    print(user_id)
    paid = get_user_done_paid_orders(user_id)

    await message.answer(f"""
💰 Баланс : {paid}

        """, parse_mode="HTML")
