from aiogram import Router, F
from aiogram.types import CallbackQuery
from db.manager import get_user_by_id, get_user_order_stats
from keyboard.manager import back_to_managers_button
from typing import Union, List
from aiogram.filters import BaseFilter, Command
from aiogram.types import Message
from db.manager import getManagersId

# Фильтр
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

# Ваша функция, возвращающая список ID админов


# Хендлер для админов


router = Router()

@router.callback_query(F.data.startswith("user_"), ChatTypeFilter(getManagersId()))
async def handle_user_detail(callback: CallbackQuery):
    try:
        user_id = int(callback.data.split("_")[1])
    except (IndexError, ValueError):
        await callback.answer("Некорректный ID пользователя.")
        return
    print(user_id)
    user = get_user_by_id(user_id)
    print(user)

    if not user:
        await callback.answer("Пользователь не найден.")
        return

    stats = get_user_order_stats(str(user['TelegramId']))

    text = (
        f"👤 <b>Профиль мастера</b>\n\n"
        f"🆔 ID: <code>{user['Id']}</code>\n"
        f"📛 Имя: <b>{user['Name']}</b>\n"
        # f"📞 Телефон: <code>{user['Phone']}</code>\n\n"
        f"📊 <b>Статистика заказов:</b>\n"
            f"✅ Выполнено: <b>{stats['count']}</b>\n"
        # f"💸 Клиент заплатил: <b>{stats['total_price']} ₽</b>\n"
        # f"👷 Мастер получил: <b>{stats['total_worker_price']} ₽</b>\n"
        # f"касса : <b>{stats['total_price'] - stats['total_worker_price']} ₽</b>"
    )

    # Возврат на список пользователей, передаём текущую страницу (например, 0)
    keyboard = back_to_managers_button(id=user['TelegramId'])

    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")
    await callback.answer()
