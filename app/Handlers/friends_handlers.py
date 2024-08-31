from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.Handlers.messages_handlers import inline_users
from app.Repositories.accountsRepository import AccountsRepository
from app.Repositories.friendsRepository import FriendsRepository
from app.Resources.texts.namings import TableNames
from app.StatesModels.Friend.createFriendDto import CreateFriendsDto
from app.handlers import CRUD_button_with_table, users_ids

router = Router()


@router.callback_query(F.data.startswith("friends"))
async def CRUD_friends(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data.endswith("add"):

        if callback_query.from_user.id in users_ids.keys():
            id = users_ids[callback_query.from_user.id]

            await state.set_state(CreateFriendsDto.account_id)
            await state.update_data(account_id=id)
            await state.set_state(CreateFriendsDto.friend_id)

            await callback_query.message.answer("Выберите, с кем подружиться",
                                                reply_markup=await inline_accounts_without_user_by(int(id)))
        else:
            await state.set_state(CreateFriendsDto.account_id)
            await callback_query.message.answer("Выберите, кого дружить",
                                                reply_markup=await inline_users())

    if callback_query.data.endswith("list"):
        await getFriends(callback_query.message)


async def inline_accounts_without_user_by(id: int):
    df = await AccountsRepository.getAll()

    df_without_user = df[df['id'] != id]

    builder = InlineKeyboardBuilder()
    for item in df_without_user.values.tolist():
        df_user = await AccountsRepository.getById(int(item[0]))
        name = df_user["Fullname"][0]

        builder.add(InlineKeyboardButton(text=name, callback_data=f"{item[0]}"))

    builder.adjust(2)

    return builder.as_markup()


@router.callback_query(CreateFriendsDto.account_id)
async def add_friends(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(account_id=callback_query.data)
    await state.set_state(CreateFriendsDto.friend_id)

    await callback_query.message.answer("Выберите, с кем подружиться",
                                        reply_markup=await inline_accounts_without_user_by(int(callback_query.data)))


@router.callback_query(CreateFriendsDto.friend_id)
async def add_friends_friend_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(friend_id=callback_query.data)
    await state.set_state(CreateFriendsDto.friend_id)

    data = await state.get_data()
    await state.clear()

    result = await FriendsRepository.add(int(data["account_id"]), int(data["friend_id"]))

    if type(result) is bool and result == True:
        await callback_query.message.answer(f"Теперь эти люди дружат друг с другом")
    else:
        await callback_query.message.answer(f"Отправить не удалось. {result}")

    await getFriends(callback_query.message)


@router.message(F.text == "Друзья")
async def getFriends(message: Message):
    df = await getFriendsDto()

    await CRUD_button_with_table(message, df, "friends")


async def getFriendsDto():
    df = await FriendsRepository.getAll()

    df.set_index('id', inplace=True)

    return df
