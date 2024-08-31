from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F, Router

from app.Repositories.subscriptionsRepository import SubscriptionsRepository
from app.Resources.texts.namings import TableNames
from app.handlers import CRUD_button_with_table

router = Router()


@router.message(F.text == "Подписчики групп")
async def getSubscriptions(message: Message):
    df = await SubscriptionsRepository.getAll()

    df.set_index('id', inplace=True)

    await CRUD_button_with_table(message, df, "subscriptions")


@router.callback_query(F.data.startswith(TableNames.messages))
async def CRUD_session(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.endswith("list"):
        await getSubscriptions(callback_query.message)
