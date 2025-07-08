from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu_manager():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Работники")],
            [KeyboardButton(text="Заказы")],
            # [KeyboardButton(text="")],

        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )










def get_manager_keyboard(users: list, page: int) -> InlineKeyboardMarkup:
    buttons = []

    # Кнопки пользователей
    for user in users:
        buttons.append([
            InlineKeyboardButton(
                text=f"{user['Name']} (ID: {user['TelegramId']})",
                callback_data=f"user_{user['TelegramId']}"
            )
        ])
    buttons.append([InlineKeyboardButton(
                text="Добавить работника",
                callback_data=f"add_user"
            )])

    # Кнопки пагинации
    pagination = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"user_prev_{page - 1}"
            )
        )
    pagination.append(
        InlineKeyboardButton(
            text="➡️ Далее",
            callback_data=f"user_next_{page + 1}"
        )
    )
    if pagination:
        buttons.append(pagination)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_managers_button(id) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к списку", callback_data=f"user_prev_0"), InlineKeyboardButton(text="Удалить работника", callback_data=f"del_user_{id}")]
        ]
    )


def confirm_cancel_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm"),
                InlineKeyboardButton(text="❌ Отменить", callback_data="cancel"),
            ]
        ]
    )

def cancel_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def confirm_delete_kb(user_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"confirm_del_user_{user_id}")],
        [InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_del")]
    ])




def get_orders_keyboard(orders: list, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = []

    for order in orders:
        text = f"#{order['Id']} — {order['Adress']}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"order_manage_{order['Id']}"
            )
        ])

    nav_buttons = []
    keyboard.append([InlineKeyboardButton(
        text="Добавить заказ",
        callback_data=f"add_order_manager"
    )])

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"prev_manager_{page - 1}"))
    if len(orders) == 5:  # Если ровно 5 заказов, значит, может быть следующая страница
        nav_buttons.append(InlineKeyboardButton(text="➡ Вперёд", callback_data=f"next_manager_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def back_to_orders_button(page: int = 0, id: int = 0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад к заказам", callback_data=f"page_manager_{page}"),
             InlineKeyboardButton(text="🗑 Удалить", callback_data=f"order_confirm_remove_{id}")
            ]
        ]
    )
