import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from matplotlib import pyplot as plt

import app.keyboards as kb
from app.Repositories.groupsRepository import GroupsRepository
from app.Repositories.subscriptionsRepository import SubscriptionsRepository

from app.Resources.texts.namings import d_ent_func
from app.StatesModels.Group.getAverageAgeInGroupDto import GetAverageAgeInGroup
from app.handlers import df_empty, answer_dataframe
from settings import path_images

import seaborn as sns

router = Router()


@router.message(F.text == d_ent_func[4])
async def create_func_subscribers_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_subscribers_buttons)


@router.message(F.text == "Предложения друзей пользователя на основе общ. групп")
async def getSuggestGroupFriendsForAllResidents(message: Message):
    df = await SubscriptionsRepository.getSuggestGroupFriendsForAllResidents()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await answer_dataframe(df, message)


async def inline_groups():
    df = await GroupsRepository.getAll()
    data = df.values.tolist()

    builder = InlineKeyboardBuilder()
    for row in data:
        df_group = await GroupsRepository.get(int(row[0]))
        name = df_group["Name"][0]

        builder.add(InlineKeyboardButton(text=name, callback_data=f"{row[0]}"))

    builder.adjust(2)

    return builder.as_markup()


@router.message(F.text == "Ср. возраст пользователей группы")
async def getAverageAgeInGroup(message: Message, state: FSMContext):
    await state.set_state(GetAverageAgeInGroup.group_id)
    await message.answer("Выберите группу", reply_markup=await inline_groups())


@router.message(GetAverageAgeInGroup.group_id)
async def getAverageAgeInGroup_group_id(message: Message, state: FSMContext):
    await state.update_data(group_id=message.text)
    data = await state.get_data()
    await state.clear()

    df = await SubscriptionsRepository.getAverageAgeInGroup(int(data["group_id"]))

    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Ср. возраст участников каждой группы")
async def getFriendlyUser(message: Message):
    df = await SubscriptionsRepository.getAverageAgeInGroups()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await plot_average_age_in_groups(df, message)


async def plot_average_age_in_groups(df: pd.DataFrame, message: Message):

    plt.figure(figsize=(14, 7))
    sns.barplot(x='Средний_возраст', y='Название', data=df, palette='coolwarm')

    plt.title('Средний возраст участников в каждой группе')
    plt.xlabel('Средний возраст')
    plt.ylabel('Группа')

    png = path_images + "average_age_in_groups.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption='Средний возраст участников в каждой группе',
        photo=FSInputFile(path=png))
