from create_bot import bot
from db.manager import get_user_by_id, getOrder, getManagersId

async def worker_start_order(params):
    order = getOrder(params['order'])
    user = get_user_by_id(user_id=params['id'])
    print(getManagersId, order, user)
    text = (
        f"🟡 <b>Работник начал выполнение заказа</b>\n\n"
        f"👤 <b>Работник:</b> {user['Name']} @{user['UserName']}\n"
        f"📦 <b>Заказ №{order['Id']}</b>\n"
        f"📍 <b>Адрес:</b> {order['Adress']}\n"


        f"📅 <b>Дата начала:</b> {order['dateStarted']}\n"
        f"📞 <b>Клиент:</b> {order['FullName']} ({order['Phone']})"
    )
    for i in getManagersId():

        await bot.send_message(i, text,  parse_mode="HTML")

async def worker_confirm_order(params):
    order = getOrder(params['order'])
    user = get_user_by_id(user_id=params['id'])
    text = (
        f"✅ <b>Работник завершил заказ</b>\n\n"
        f"👤 <b>Работник:</b> {user['Name']} @{user['UserName']}\n"
        f"📦 <b>Заказ №{order['Id']}</b>\n"
        f"📍 <b>Адрес:</b> {order['Adress']}\n"
        f"🕓 <b>Дата завершения:</b> {order['dateDone']}\n"

    )
    for i in getManagersId():
        await bot.send_message(i, text, parse_mode="HTML")