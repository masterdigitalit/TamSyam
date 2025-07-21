from create_bot import bot
from db.admin import getOwnersId
async def manager_add_worker(params: dict):
    name = params.get("name", "Без имени")
    telegram_name = params.get("username", "Не указан")
    managername = params.get("manager_name","")





    text = (
        f"➕ <b>Добавлен новый работник</b>\n\n"
        f"👤 <b>Имя:</b> {name}\n"
        f"🆔 <b>Telegram:</b> @{telegram_name}\n"
        f"🆔 <b>Добавил:</b> @{managername}\n"

    )

    # Рассылка менеджерам
    for admin in getOwnersId():
        try:
           await bot.send_message(admin, text, parse_mode="HTML")
        except Exception as e:
            pass
