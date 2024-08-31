import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message

import app.keyboards as kb
import app.handlers as main_handlers
import app.Handlers.messages_handlers as messages_handlers
import app.Handlers.friends_handlers as friends_handlers
import app.Handlers.accounts_handlers as accounts_handlers
import app.Handlers.groups_handlers as groups_handlers
import app.Handlers.subscriptions_handlers as session_handlers
import app.Handlers.StoredProcedures.procedures_friends_handlers as procedures_friends
import app.Handlers.StoredProcedures.procedures_accounts_handlers as procedures_accounts
import app.Handlers.StoredProcedures.procedures_messages_handlers as procedures_messages
import app.Handlers.StoredProcedures.procedures_groups_handlers as procedures_groups
import app.Handlers.StoredProcedures.procedures_subscribers_handlers as procedures_subscribers

from aiogram.client.session.aiohttp import AiohttpSession

from app.token import token

chat_ids = [463609327]


async def main():
    bot = Bot(token=token, proxy='http://proxy.server:3128')

    if all(not array for array in main_handlers.register_role.values()):
        for chat_id in chat_ids:
            await bot.send_message(
                chat_id,
                'Добро пожаловать в мини социальную сеть! Требуется выбрать роль',
                reply_markup=kb.mainButtons)

    # Управляет хэндлерами
    dp = Dispatcher()

    dp.include_router(main_handlers.router)
    dp.include_routers(
        messages_handlers.router,
        friends_handlers.router,
        session_handlers.router,
        accounts_handlers.router,
        groups_handlers.router,
        procedures_friends.router,
        procedures_accounts.router,
        procedures_messages.router,
        procedures_groups.router,
        procedures_subscribers.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
