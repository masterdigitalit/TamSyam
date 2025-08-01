from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from manager.notification import   worker_confirm_order
from db.user import confirmOrder
from create_bot import bot
from keyboard.user import cancel_reply_keyboard, main_menu_worker

router = Router()



def get_confirm_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="short_confirm")],
        [InlineKeyboardButton(text="🔁 Заполнить заново", callback_data="short_restart")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="short_cancel")]
    ])



class BuyOneShortState(StatesGroup):
    price = State()
    id = State()
    confirm = State()



@router.callback_query(F.data.startswith("confirm_my_"))
async def start_buy_one(callback_query: CallbackQuery, state: FSMContext):
    try:
        order_id = int(callback_query.data.replace("confirm_my_", ""))
        await state.clear()
        await state.update_data(id=order_id)
        await state.set_state(BuyOneShortState.price)
        await callback_query.message.answer("💰 Введите цену заказа (например: 1500):", reply_markup=cancel_reply_keyboard())
    except ValueError:
        await callback_query.answer("❌ Ошибка: неверный формат ID", show_alert=True)



@router.message(BuyOneShortState.price)
async def set_price(message: Message, state: FSMContext):
    text = message.text.strip().lower()



    if text in ["❌ отменить", "❌ Отменить"]:
        await state.clear()
        await message.answer("❌ Заказ отменён.", reply_markup=main_menu_worker())
        return

    if not text.isdigit():
        await message.answer("⚠ Цена должна быть числом. Введите корректно:")
        return

    await state.update_data(price=text)
    data = await state.get_data()

    summary = (
        f"<b>Проверьте данные:</b>\n\n"
        f"<b>Цена:</b> {data['price']} ₽"
    )

    await state.set_state(BuyOneShortState.confirm)
    await message.answer(summary, parse_mode="HTML", reply_markup=get_confirm_keyboard())



@router.callback_query(BuyOneShortState.confirm, F.data == "short_confirm")
async def confirm_order(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    order_id = data.get("id")
    price = data.get("price")

    if order_id is None or price is None:
        await callback_query.answer("⚠ Ошибка: отсутствуют данные заказа.", show_alert=True)
        await state.clear()
        return

    confirmOrder(id=order_id, comment="", price=price)
    await worker_confirm_order({"order":order_id, "id":callback_query.from_user.id})


    await state.clear()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "✅ Заказ успешно помечен как выполненный.", reply_markup=main_menu_worker())



@router.callback_query(BuyOneShortState.confirm, F.data == "short_restart")
async def restart_form(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_id = data.get("id")

    await state.clear()
    await state.update_data(id=order_id)
    await state.set_state(BuyOneShortState.price)
    await callback_query.message.answer("🔁 Введите цену заказа:", reply_markup=cancel_reply_keyboard())


@router.callback_query(BuyOneShortState.confirm, F.data == "short_cancel")
async def cancel_inline(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "❌ Заказ отменён.", reply_markup=main_menu_worker())



@router.message(F.text.lower().in_({"отмена", "❌ отмена"}))
async def cancel_fallback(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Действие отменено.", reply_markup=main_menu_worker())
