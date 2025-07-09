from aiogram import Router, F
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from db.manager import addOrderFromManager

from typing import Union, List
from aiogram.filters import BaseFilter
from aiogram.types import Message
from db.manager import getManagersId


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







router = Router()



class AddOrderManagerState(StatesGroup):
    adress = State()
    name = State()
    phone = State()
    desc = State()
    confirm = State()



def cancel_keyboard(callback: str = "cancel_add_order"):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отмена", callback_data=callback)]
    ])



@router.callback_query(F.data == "add_order_manager", ChatTypeFilter(getManagersId()))
async def start_add_order(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddOrderManagerState.adress)
    await callback.message.edit_text("📍 Введите адрес заказа:", reply_markup=cancel_keyboard())
    await callback.answer()



@router.message(AddOrderManagerState.adress, ChatTypeFilter(getManagersId()))
async def add_adress(msg: Message, state: FSMContext):
    await state.update_data(adress=msg.text)
    await state.set_state(AddOrderManagerState.name)
    await msg.answer("🙍‍♂️ Введите имя клиента:", reply_markup=cancel_keyboard())



@router.message(AddOrderManagerState.name, ChatTypeFilter(getManagersId()))
async def add_name(msg: Message, state: FSMContext):
    await state.update_data(name=msg.text)
    await state.set_state(AddOrderManagerState.phone)
    await msg.answer("📞 Введите номер телефона:", reply_markup=cancel_keyboard())



@router.message(AddOrderManagerState.phone, ChatTypeFilter(getManagersId()))
async def add_phone(msg: Message, state: FSMContext):
    await state.update_data(phone=msg.text)
    await state.set_state(AddOrderManagerState.desc)
    await msg.answer("📝 Введите описание заказа:", reply_markup=cancel_keyboard())



@router.message(AddOrderManagerState.desc, ChatTypeFilter(getManagersId()))
async def add_desc(msg: Message, state: FSMContext):
    await state.update_data(desc=msg.text)
    data = await state.get_data()

    text = (
        f"🆕 Новый заказ:\n\n"
        f"📍 Адрес: {data['adress']}\n"
        f"🙍‍♂️ Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📝 Описание: {data['desc']}\n\n"
        f"Подтвердить?"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_add_order")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_add_order")]
    ])
    await state.set_state(AddOrderManagerState.confirm)
    await msg.answer(text, reply_markup=kb)



@router.callback_query(F.data == "confirm_add_order", ChatTypeFilter(getManagersId()))
async def confirm_add(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()


    addOrderFromManager(
        adress=data['adress'],
        name=data['name'],
        phone=data['phone'],
        desc=data['desc']
    )

    await callback.message.edit_text("✅ Заказ успешно добавлен.")
    await state.clear()
    await callback.answer()



@router.callback_query(F.data == "cancel_add_order", ChatTypeFilter(getManagersId()))
async def cancel_add(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.answer()
    await callback.message.edit_text(
        text="❌ Добавление заказа отменено.",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅ Назад к заказам", callback_data="page_manager_0")]
            ]
        )
    )
