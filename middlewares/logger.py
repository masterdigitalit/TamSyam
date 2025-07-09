from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any
from app_logger import logger

class MessageLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        logger.info(f"📩 Сообщение от @{user.username or user.id}: {event.text}")
        return await handler(event, data)


class CallbackLoggerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        user = event.from_user
        logger.info(f"🟢 Callback от @{user.username or user.id}: {event.data}")
        return await handler(event, data)
