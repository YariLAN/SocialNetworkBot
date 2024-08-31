from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.DbModels.Message import MessageMapper

import app.StatesModels.Message.createMessageDto as dto
from app.Repositories.accountsRepository import AccountsRepository
from app.Repositories.friendsRepository import FriendsRepository
from app.Repositories.messageRepository import MessageRepository
from app.Resources.texts.namings import TableNames
from app.handlers import CRUD_button_with_table, users_ids

router = Router()


@router.callback_query(F.data.startswith(TableNames.messages))
async def CRUD_message(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.endswith("add"):

        if callback_query.from_user.id in users_ids.keys():
            id = users_ids[callback_query.from_user.id]

            await state.set_state(dto.CreateMessageDto.sender_id)
            await state.update_data(sender_id=id)
            await state.set_state(dto.CreateMessageDto.recipient_id)

            await callback_query.message.answer("Выберите, кому отправите письмо",
                                                reply_markup=await inline_recipients(int(id)))
        else:
            await state.set_state(dto.CreateMessageDto.sender_id)
            await callback_query.message.answer("Выберите пользователя, от которого пойдет письмо",
                                                reply_markup=await inline_users())

    if callback_query.data.endswith("list"):
        await getMessages(callback_query.message)


async def inline_users():
    df = await AccountsRepository.getAll()
    data = df.values.tolist()

    builder = InlineKeyboardBuilder()
    for row in data:
        df_user = await AccountsRepository.getById(int(row[0]))
        name = df_user["Fullname"][0]

        builder.add(InlineKeyboardButton(text=name, callback_data=f"{row[0]}"))

    builder.adjust(2)

    return builder.as_markup()


async def inline_recipients(user_id: int):
    df = await FriendsRepository.getByFriendId(user_id)
    data = df.values.tolist()

    builder = InlineKeyboardBuilder()
    for row in data:
        df_user = await AccountsRepository.getById(int(row[2]))
        name = df_user["Fullname"][0]

        builder.add(InlineKeyboardButton(text=name, callback_data=f"{row[2]}"))

    builder.adjust(2)

    return builder.as_markup()


# Добавление фильма
@router.callback_query(dto.CreateMessageDto.sender_id)
async def add_message_sender_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(sender_id=callback_query.data)

    await state.set_state(dto.CreateMessageDto.recipient_id)
    await callback_query.message.answer("Выберите друга, которому отправите письмо",
                                        reply_markup=await inline_recipients(int(callback_query.data)))


@router.callback_query(dto.CreateMessageDto.recipient_id)
async def add_message_recipient_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(recipient_id=callback_query.data)

    await state.set_state(dto.CreateMessageDto.text)
    await callback_query.message.answer("Введите сообщение")


@router.message(dto.CreateMessageDto.text)
async def add_message_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)

    data = await state.get_data()

    result = await MessageRepository.add(
        MessageMapper.toMap(data["sender_id"], data["recipient_id"], data["text"]))

    if result:
        await message.answer(f"Сообщение {data['text']} успешно отправлено")
    else:
        await message.answer(f"Отправить не удалось. {result}")

    await state.clear()
    await getMessages(message)


@router.message(F.text == "Сообщения")
async def getMessages(message: Message):
    df = await getMessagesDataframe()

    await CRUD_button_with_table(message, df, "messages")


async def getMessagesDataframe():
    df = await MessageRepository.getAll()
    df.set_index('id', inplace=True)

    return df
