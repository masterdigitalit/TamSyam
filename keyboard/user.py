from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def main_menu_worker():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Заказы"), KeyboardButton(text="Мои заказы")],
            [KeyboardButton(text="Баланс"),
             KeyboardButton(text="Менеджер")
            ],

        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def get_orders_keyboard(orders: list, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = []

    for order in orders:
        text = f"#{order['Id']} — {order['Adress']}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"order_{order['Id']}"
            )
        ])

    nav_buttons = []

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"prev_{page - 1}"))
    if len(orders) == 5:  # Если ровно 5 заказов, значит, может быть следующая страница
        nav_buttons.append(InlineKeyboardButton(text="➡ Вперёд", callback_data=f"next_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
def get_my_orders_keyboard(orders: list, page: int = 0) -> InlineKeyboardMarkup:
    keyboard = []

    for order in orders:
        text = f"#{order['Id']} — {order['Adress']}"
        keyboard.append([
            InlineKeyboardButton(
                text=text,
                callback_data=f"order_{order['Id']}"
            )
        ])

    nav_buttons = []

    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅ Назад", callback_data=f"prev_my_{page - 1}"))
    if len(orders) == 5:  # Если ровно 5 заказов, значит, может быть следующая страница
        nav_buttons.append(InlineKeyboardButton(text="➡ Вперёд", callback_data=f"next_my_{page + 1}"))

    if nav_buttons:
        keyboard.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=keyboard)




def back_to_orders_button(page: int = 0, id : int = 0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад к заказам", callback_data=f"page_{page}"),
             InlineKeyboardButton(text="✅ Приступить", callback_data=f"start_{id}")
            ]
        ]
    )
def back_to_my_orders_button(page: int = 0, id : int = 0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад к заказам", callback_data=f"prev_my_0"),
             InlineKeyboardButton(text="✅ Подтвердить выполнение", callback_data=f"confirm_my_{id}")
            ]
        ]
    )

def cancel_reply_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отменить")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Напишите ответ или нажмите кнопку отмены"
    )