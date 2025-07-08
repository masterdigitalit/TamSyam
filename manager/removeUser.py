from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from typing import Union, List

from db.manager import deleteUserFromManager, getManagersId
from keyboard.manager import main_menu_manager, confirm_delete_kb
from create_bot import bot

router = Router()

# ======= Фильтр по ID менеджеров =======
class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        if isinstance(user_id, int):
            self.user_ids = [user_id]
        else:
            self.user_ids = user_id or []

    async def __call__(self, callback: CallbackQuery) -> bool:
        print(f"[FILTER] from_user.id = {callback.from_user.id}")
        print(f"[FILTER] self.user_ids = {self.user_ids}")
        return callback.from_user.id in self.user_ids


# ======= 1. Нажали «Удалить работника» =======
@router.callback_query(F.data.startswith("del_user_"), ChatTypeFilter(user_id=getManagersId()))
async def confirm_delete_worker(callback: CallbackQuery, state: FSMContext):
    worker_id_str = callback.data.split("_")[-1]

    if not worker_id_str.isdigit():
        await callback.answer("❌ Неверный формат ID.")
        return

    worker_id = int(worker_id_str)

    await callback.message.edit_text(
        f"❗ Вы уверены, что хотите удалить работника с Telegram ID <code>{worker_id}</code>?",
        parse_mode="HTML",
        reply_markup=confirm_delete_kb(worker_id)
    )
    await state.clear()


# ======= 2. Подтвердили удаление =======
@router.callback_query(F.data.startswith("confirm_del_user_"), ChatTypeFilter(user_id=getManagersId()))
async def delete_worker(callback: CallbackQuery, state: FSMContext):
    worker_id_str = callback.data.split("_")[-1]

    if not worker_id_str.isdigit():
        await callback.answer("❌ Неверный ID.")
        return

    worker_id = int(worker_id_str)

    success = deleteUserFromManager(worker_id)

    if success:
        await bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            text=f"✅ Работник с Telegram ID <code>{worker_id}</code> удалён.",
            parse_mode="HTML"
        )
    else:
        await callback.answer("❌ Не удалось удалить работника. Возможно, он уже удалён.", show_alert=True)

    await state.clear()


# ======= 3. Отменили удаление =======
@router.callback_query(F.data == "cancel_del", ChatTypeFilter(user_id=getManagersId()))
async def cancel_delete_worker(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Удаление отменено.", reply_markup=main_menu_manager())
    await state.clear()
