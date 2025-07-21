from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import BaseFilter
from typing import Union, List

from db.admin import delete_manager_by_id, getOwnersId


router = Router()


class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id or []

    async def __call__(self, message_or_callback: Union[Message, CallbackQuery]) -> bool:
        user_id = (
            message_or_callback.from_user.id
            if isinstance(message_or_callback, (Message, CallbackQuery))
            else None
        )
        return user_id in self.user_ids


def get_remove_manager_confirm_kb(manager_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить удаление", callback_data=f"confirm_remove_manager_{manager_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data=f"cancel_remove_manager_{manager_id}")]
    ])


@router.callback_query(F.data.startswith("remove_manager_"), ChatTypeFilter(user_id=getOwnersId()))
async def start_remove_manager(callback: CallbackQuery, state: FSMContext):
    manager_id = callback.data.split("_")[-1]

    if not manager_id.isdigit():
        await callback.answer("❌ Неверный ID менеджера.")
        return

    manager_id = int(manager_id)

    await callback.message.edit_text(
        f"⚠️ Вы уверены, что хотите удалить менеджера с ID <code>{manager_id}</code>?",
        reply_markup=get_remove_manager_confirm_kb(manager_id),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("confirm_remove_manager_"), ChatTypeFilter(user_id=getOwnersId()))
async def confirm_remove_manager(callback: CallbackQuery, state: FSMContext):
    manager_id = callback.data.split("_")[-1]

    if not manager_id.isdigit():
        await callback.answer("❌ Неверный ID.")
        return

    manager_id = int(manager_id)
    success = delete_manager_by_id(manager_id)  # 💾

    if success:
        await callback.message.edit_text(
            f"✅ Менеджер с ID <code>{manager_id}</code> успешно удалён.",
            parse_mode="HTML"
        )
    else:
        await callback.answer("❌ Не удалось удалить менеджера. Возможно, он уже удалён.", show_alert=True)

    await state.clear()


@router.callback_query(F.data.startswith("cancel_remove_manager_"), ChatTypeFilter(user_id=getOwnersId()))
async def cancel_remove_manager(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Удаление менеджера отменено.")
    await state.clear()
