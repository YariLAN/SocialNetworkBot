from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb
from app.Handlers.messages_handlers import inline_users
from app.Repositories.messageRepository import MessageRepository
from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Message.getUserMessagesDto import GetUserMessagesDto
from app.handlers import df_empty, answer_dataframe, users_ids

router = Router()


@router.message(F.text == d_ent_func[3])
async def create_func_messages_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_messages_buttons)


@router.message(F.text == "Список сообщений пользователя")
async def getUserMessages(message: Message, state: FSMContext):
    await state.set_state(GetUserMessagesDto.account_id)
    await message.answer("Выберите пользователя", reply_markup=await inline_users())


@router.callback_query(GetUserMessagesDto.account_id)
async def getUserMessages_account_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(account_id=callback_query.data)
    data = await state.get_data()
    await state.clear()

    df = await MessageRepository.getUserMessages(int(data["account_id"]))

    if df.empty:
        await df_empty(df, callback_query.message)
    else:
        await answer_dataframe(df, callback_query.message)
