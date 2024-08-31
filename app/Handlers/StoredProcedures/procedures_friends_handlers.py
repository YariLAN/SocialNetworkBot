import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from matplotlib import pyplot as plt

import app.keyboards as kb
from app.Handlers.messages_handlers import inline_users
from app.Repositories.friendsRepository import FriendsRepository
from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Friend.getFriendsDto import GetFriendsDto
from app.handlers import df_empty, answer_dataframe
from settings import path_images

router = Router()


async def init_additional_buttons(message: Message):
    await message.answer("Выберите сущность для работы с дополнительными функциями",
                         reply_markup=kb.additional_buttons)


@router.message(F.text == "Дополнительные функции")
async def create_additional_functions_keyboard(message: Message):
    await message.delete()
    await init_additional_buttons(message)


@router.message(F.text == d_ent_func[0])
async def create_func_friends_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_friends_buttons)


@router.message(F.text == "Назад")
async def go_back(message: Message):
    await init_additional_buttons(message)


@router.message(F.text == "Список друзей пользователя")
async def get_friends(message: Message, state: FSMContext):
    await state.set_state(GetFriendsDto.account_id)
    await message.answer("Выберите пользователя", reply_markup=await inline_users())


@router.callback_query(GetFriendsDto.account_id)
async def get_friends_account_id(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(account_id=callback_query.data)
    data = await state.get_data()
    await state.clear()

    df = await FriendsRepository.getByUserId(int(data["account_id"]))

    if df.empty:
        await df_empty(df, callback_query.message)
    elif 'Exception' in df.columns:
        await answer_dataframe(df, callback_query.message)
    else:
        await answer_dataframe(df, callback_query.message)


@router.message(F.text == "Дружелюбный пользователь")
async def getFriendlyUser(message: Message):
    df = await FriendsRepository.getMostFriendlyResident()

    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Кол-во друзей у топ-10 пользователей")
async def getDailyRevenueByFilm(message: Message):
    df = await FriendsRepository.getCountFriends()
    df = df.sort_values(by='Количество_друзей', ascending=False)

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await plot_friends_count_pie_chart(message, df)


async def plot_friends_count_pie_chart(message: Message, df: pd.DataFrame):

    top_n = 10
    top_users = df.head(top_n)
    other_users_count = df['Количество_друзей'][top_n:].sum()

    labels = top_users['Fullname'].tolist() + ['Другие']
    sizes = top_users['Количество_друзей'].tolist() + [other_users_count]

    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Количество друзей у топ-10 пользователей')

    png = path_images + "friends_count_pie_chart.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Количество друзей у топ-10 пользователей',
        photo=FSInputFile(path=png))
