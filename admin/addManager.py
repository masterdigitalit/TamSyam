from aiogram import Router, F
from aiogram.types import (
    CallbackQuery, Message,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import BaseFilter
from typing import Union, List

from create_bot import bot
from keyboard.admin import main_menu_admin
from db.admin import getAdminsId, addManager, is_manager_exists

router = Router()


class AddManagerState(StatesGroup):
    fio = State()
    telegram_id = State()
    confirm = State()


def get_manager_confirm_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="add_manager_confirm")],
        [InlineKeyboardButton(text="🔁 Заполнить заново", callback_data="add_manager_restart")],
        [InlineKeyboardButton(text="❌ Отменить", callback_data="add_manager_cancel")]
    ])


def cancel_inline_start():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить", callback_data="add_manager_cancel")]
    ])


def cancel_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


class ChatTypeFilter(BaseFilter):
    def __init__(self, user_id: Union[int, List[int]]):
        self.user_ids = [user_id] if isinstance(user_id, int) else user_id or []

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.user_ids


@router.callback_query(F.data == "add_manager_admin", ChatTypeFilter(user_id=getAdminsId()))
async def add_manager_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AddManagerState.fio)
    await bot.send_message(callback.from_user.id, "📝 Введите ФИО менеджера одним сообщением:", reply_markup=cancel_inline_start())


@router.message(AddManagerState.fio, ChatTypeFilter(user_id=getAdminsId()))
async def add_manager_fio(message: Message, state: FSMContext):
    await state.update_data(fio=message.text.strip())
    await state.set_state(AddManagerState.telegram_id)
    await message.answer("📩 Перешли сообщение от менеджера (чтобы получить Telegram ID):", reply_markup=cancel_inline_start())


@router.message(AddManagerState.telegram_id, ChatTypeFilter(user_id=getAdminsId()))
async def add_manager_forward(message: Message, state: FSMContext):
    text = message.text.strip().lower() if message.text else ""

    if text in {"отмена", "❌ отмена"}:
        await state.clear()
        await bot.send_message(
            chat_id=message.from_user.id,
            text="❌ Добавление менеджера отменено.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="⬅ Назад к менеджерам", callback_data="manager_next_0")]
                ]
            )
        )
        return

    if not message.forward_from:
        await message.answer("❌ Это не пересланное сообщение. Пожалуйста, пересылай сообщение от менеджера.")
        return

    telegram_id = message.forward_from.id
    name = f"{message.forward_from.first_name or ''} {message.forward_from.last_name or ''}".strip()
    username = message.forward_from.username or "-"

    await state.update_data(telegram_id=telegram_id, forward_name=name, username=username)
    data = await state.get_data()

    await state.set_state(AddManagerState.confirm)

    await message.answer(
        f"🔎 <b>Проверьте данные:</b>\n\n"
        f"👤 ФИО: <b>{data['fio']}</b>\n"
        f"🔐 Telegram ID: <code>{telegram_id}</code>\n"
        f"👤 Имя в Telegram: <b>{name}</b>\n"
        f"{'🔗 Username: <b>@' + username + '</b>' if username != '-' else '🔗 Username: <i>не указан</i>'}",
        reply_markup=get_manager_confirm_kb(),
        parse_mode="HTML"
    )


@router.callback_query(AddManagerState.confirm, F.data == "add_manager_confirm", ChatTypeFilter(user_id=getAdminsId()))
async def confirm_add_manager(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()


    if is_manager_exists(data['telegram_id']):
        await bot.send_message(
            callback_query.from_user.id,
            f"⚠ Менеджер с таким Telegram ID уже существует.",
            parse_mode="HTML",
            reply_markup=main_menu_admin()
        )
        await state.clear()
        return

    addManager(
        telegramId=data['telegram_id'],
        Name=data['fio'],
        UserName=data["username"]
    )

    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        f"✅ Менеджер добавлен:\n<b>{data['fio']}</b>",
        parse_mode="HTML",
        reply_markup=main_menu_admin()
    )
    await state.clear()

@router.callback_query(AddManagerState.confirm, F.data == "add_manager_restart", ChatTypeFilter(user_id=getAdminsId()))
async def restart_manager(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(AddManagerState.fio)
    await bot.send_message(callback_query.from_user.id, "🔁 Введите ФИО менеджера:", reply_markup=cancel_inline_start())


@router.callback_query(F.data == "add_manager_cancel", ChatTypeFilter(user_id=getAdminsId()))
async def cancel_manager_inline(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(
        callback_query.from_user.id,
        text="❌ Добавление менеджера отменено.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅ Назад к менеджерам", callback_data="manager_next_0")]
            ]
        )
    )
