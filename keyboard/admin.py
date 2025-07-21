from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_users_keyboard(users, page: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)

    for user in users:
        keyboard.add(InlineKeyboardButton(
            text=f"{user['FullName']} (ID: {user['Id']})",
            callback_data=f"user_{user['Id']}"
        ))

    # Пагинация
    pagination = []
    if page > 0:
        pagination.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"user_prev_{page - 1}"))
    pagination.append(InlineKeyboardButton("➡️ Далее", callback_data=f"user_next_{page + 1}"))
    keyboard.row(*pagination)

    return keyboard


def main_menu_admin():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Статистика")],
            [KeyboardButton(text="Менеджеры")],
            [KeyboardButton(text="Таблица")],[KeyboardButton(text="Добавить заказ")]


        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )


def statistic_menu_admin():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📅 За сегодня", callback_data="stat_today"),
                InlineKeyboardButton(text="📊 За все время", callback_data="stat_all"),
                InlineKeyboardButton(text="📊 По месяцам", callback_data="stat_show_month")
            ]
        ]
    )



def statistic_menu_next():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Назад", callback_data="stat_menu"),

            ]
        ]
    )







def get_manager_keyboard(users: list, page: int) -> InlineKeyboardMarkup:
    buttons = []

    # Кнопки пользователей
    for user in users:
        buttons.append([
            InlineKeyboardButton(
                text=f"{user['Name']} (ID: {user['TelegramId']})",
                callback_data=f"manager_{user['TelegramId']}"
            )
        ])
    buttons.append([InlineKeyboardButton(
                    text="Добавить менеджера",
                    callback_data=f"add_manager_admin"
                )])


    # Кнопки пагинации
    pagination = []
    if page > 0:
        pagination.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data=f"manager_prev_{page - 1}"
            )
        )
    pagination.append(
        InlineKeyboardButton(
            text="➡️ Далее",
            callback_data=f"manager_next_{page + 1}"
        )
    )
    if pagination:
        buttons.append(pagination)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_managers_button(id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад к списку", callback_data=f"manager_prev_0"),InlineKeyboardButton(text="Удалить менеджера", callback_data=f"remove_manager_{id}") ]
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

def build_months_keyboard(months: list) -> InlineKeyboardMarkup:
    """
    Принимает список словарей с ключами "Название" и "Ключ"
    и возвращает InlineKeyboardMarkup.
    """
    builder = InlineKeyboardBuilder()

    for month in months:
        builder.button(
            text=month["Name"],
            callback_data=f"month_stat_{month['Key']}"
        )

    builder.adjust(2)  # по 2 кнопки в ряд
    return builder.as_markup()



