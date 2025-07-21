import asyncio
import traceback
from aiogram import Bot
from app_logger import logger
from create_bot import dp, bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from user import startUser, showOrdersUser, showOrderToUser, startOrder, showMyOrders, confirmComplete, showBalance
from admin import startAdmin, showStatistics, showManagers, showManagerInfo, removeManager, addManager, getExcel, addOrderFromAdmin
from manager import startManager, showUsers, showUserInfo, addUser, removeUser, manageOrder, showOrdersManager, addOrder
from middlewares.logger import MessageLoggerMiddleware, CallbackLoggerMiddleware
from db.create import init_db

ADMIN_CHAT_ID = 5273914742

dp.message.middleware(MessageLoggerMiddleware())
dp.callback_query.middleware(CallbackLoggerMiddleware())

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


async def send_error_to_admin(text: str):
    try:
        error_bot = Bot(token=bot.token)
        await error_bot.send_message(ADMIN_CHAT_ID, f"❗️CRITICAL ERROR:\n{text}")
        await error_bot.session.close()
    except Exception as e:
        logger.error(f"Не удалось отправить сообщение об ошибке администратору: {e}")


async def shutdown():
    logger.info("⛔ Завершение бота...")

    try:
        if scheduler.running:
            scheduler.shutdown(wait=False)
    except Exception as e:
        logger.error(f"Ошибка при остановке scheduler: {e}")

    try:
        await dp.storage.close()
    except Exception:
        pass

    try:
        await bot.session.close()
    except Exception:
        pass

    logger.info("✅ Всё закрыто корректно.")


async def telegram():
    init_db()
    logger.info("🤖 Бот запущен")

    scheduler.start()
    # admin
    dp.include_routers(
        showStatistics.router,
        startAdmin.router,
        showManagers.router,
        showManagerInfo.router,
        removeManager.router,
        addManager.router,
        getExcel.router,
        addOrderFromAdmin.router
    )
    # manager
    dp.include_routers(
        startManager.router,
        showUsers.router, showUserInfo.router, addUser.router, removeUser.router,
        manageOrder.router, showOrdersManager.router, addOrder.router
    )
    # user
    dp.include_routers(
        startUser.router,
        showMyOrders.router,
        showOrdersUser.router,
        showOrderToUser.router,
        startOrder.router,
        confirmComplete.router,
        showBalance.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(telegram())
    except Exception:
        err_text = traceback.format_exc()
        print("❌ Critical error — отправляю администратору и выхожу...")
        try:
            asyncio.run(send_error_to_admin(err_text))
        except RuntimeError:

            pass
        try:
            asyncio.run(shutdown())
        except RuntimeError:
            pass
