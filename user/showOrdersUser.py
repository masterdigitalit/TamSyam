from aiogram import Router, F
from aiogram.types import Message
from create_bot import bot
from db.user import get_orders, count_orders
from keyboard.user import get_orders_keyboard
from aiogram.types import CallbackQuery


router = Router()

@router.message(F.text == "Заказы")
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




@router.callback_query(F.data.startswith("next_"))
async def handle_next_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
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

@router.callback_query(F.data.startswith("prev_"))
async def handle_prev_page(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    total_pages = (total_orders + page_size - 1) // page_size

    keyboard = get_orders_keyboard(orders, page)
    text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("page_"))
async def handle_back_to_orders(callback: CallbackQuery):
    page = int(callback.data.split("_")[1])
    page_size = 5
    orders = get_orders(page, page_size)
    total_orders = count_orders()
    total_pages = (total_orders + page_size - 1) // page_size

    keyboard = get_orders_keyboard(orders, page)
    text = f"📦 Доступные заказы:\nСтраница {page + 1} из {total_pages}"
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
