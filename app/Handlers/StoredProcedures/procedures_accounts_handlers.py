import pandas as pd
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
import matplotlib.pyplot as plt

import app.keyboards as kb
from app.Repositories.accountsRepository import AccountsRepository
from app.Resources.texts.namings import d_ent_func
from app.handlers import df_empty, answer_dataframe
from settings import path_images

import seaborn as sns

router = Router()


@router.message(F.text == d_ent_func[1])
async def create_func_accounts_keyboard(message: Message):
    await message.delete()
    await message.answer("Список функций", reply_markup=kb.additional_accounts_buttons)


@router.message(F.text == "Большая разница в возрасте")
async def getFindMaxAgeDifference(message: Message):
    df = await AccountsRepository.getFindMaxAgeDifference()

    if df.empty:
        await df_empty(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Пользователь, создавший большех всех групп")
async def getFindTopGroupCreator(message: Message):
    df = await AccountsRepository.getFindTopGroupCreator()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Список влиятельных пользователей - создателей групп")
async def getInfluentialUsers(message: Message):
    df = await AccountsRepository.getInfluentialUsers()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Самые молодые пользователи")
async def getFindTopGroupCreator(message: Message):
    df = await AccountsRepository.getYoungestUsers()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await answer_dataframe(df, message)


@router.message(F.text == "Распределение возрастов")
async def getAges(message: Message):
    df = await AccountsRepository.getAges()

    if df.empty:
        await df_empty(df, message)
    elif "Exception" in df.columns:
        await answer_dataframe(df, message)
    else:
        await plot_age_distribution(message, df)


async def plot_age_distribution(message: Message, df: pd.DataFrame):
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Age'], bins=10, kde=True)

    plt.title('Распределение возрастов пользователей')
    plt.xlabel('Возраст')
    plt.ylabel('Количество')

    png = path_images + "age_distribution.png"
    plt.savefig(png, dpi=300)

    await message.answer_photo(
        caption=f'Распределение возрастов пользователей',
        photo=FSInputFile(path=png))
